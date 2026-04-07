#!/usr/bin/env python3
"""
monitor_daemon.py — Monitoramento contínuo de segurança com alertas em tempo real.
Uso:
  python monitor_daemon.py --project /caminho --start   # inicia daemon
  python monitor_daemon.py --status                     # status atual
  python monitor_daemon.py --stop                       # para o daemon
  python monitor_daemon.py --logs                       # ver logs recentes
"""
import os
import sys
import json
import time
import signal
import logging
import hashlib
import argparse
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional


# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = Path(os.environ.get('SECURITY_SKILL_RUNTIME_DIR') or (BASE_DIR.parent / '.runtime'))
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
PID_FILE    = str(RUNTIME_DIR / 'security_monitor.pid')
LOG_FILE    = str(RUNTIME_DIR / 'security_monitor.log')
STATE_FILE  = str(RUNTIME_DIR / 'security_monitor_state.json')

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

WATCH_EXTENSIONS = {'.py', '.js', '.ts', '.php', '.env', '.yml', '.yaml', '.json', '.cfg'}
IGNORED_DIRS     = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build'}

SCAN_INTERVAL_QUICK    = 6 * 3600   # 6 horas
SCAN_INTERVAL_FULL     = 24 * 3600  # 24 horas
RESCAN_DELAY_AFTER_CHANGE = 30      # segundos após mudança de arquivo


# ─── LOGGING ──────────────────────────────────────────────────────────────────

def setup_logger():
    logger = logging.getLogger('security_monitor')
    logger.setLevel(logging.INFO)
    
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    
    # Arquivo
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    
    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    
    return logger


logger = setup_logger()


# ─── ESTADO ───────────────────────────────────────────────────────────────────

def load_state() -> dict:
    try:
        return json.loads(Path(STATE_FILE).read_text())
    except Exception:
        return {
            "started_at": None,
            "last_quick_scan": None,
            "last_full_scan": None,
            "last_weekly_report": None,
            "file_hashes": {},
            "scan_history": [],
            "alerts": []
        }


def save_state(state: dict):
    Path(STATE_FILE).write_text(json.dumps(state, indent=2, default=str))


# ─── HASH DE ARQUIVOS ─────────────────────────────────────────────────────────

def hash_file(filepath: Path) -> str:
    """Calcula hash MD5 de um arquivo."""
    h = hashlib.md5()
    try:
        h.update(filepath.read_bytes())
        return h.hexdigest()
    except Exception:
        return ""


def get_project_hashes(project_path: str) -> dict:
    """Calcula hashes de todos os arquivos relevantes."""
    path = Path(project_path)
    hashes = {}
    
    for f in path.rglob('*'):
        if any(d in f.parts for d in IGNORED_DIRS):
            continue
        if f.is_file() and f.suffix in WATCH_EXTENSIONS:
            hashes[str(f)] = hash_file(f)
    
    return hashes


def detect_changes(old_hashes: dict, new_hashes: dict) -> dict:
    """Detecta arquivos modificados, adicionados e removidos."""
    changes = {"modified": [], "added": [], "removed": []}
    
    for f, h in new_hashes.items():
        if f not in old_hashes:
            changes["added"].append(f)
        elif old_hashes[f] != h:
            changes["modified"].append(f)
    
    for f in old_hashes:
        if f not in new_hashes:
            changes["removed"].append(f)
    
    return changes


# ─── SCANS ────────────────────────────────────────────────────────────────────

def run_quick_scan(project_path: str) -> dict:
    """Varredura rápida: apenas secrets e padrões críticos."""
    logger.info(f"▶ Varredura RÁPIDA iniciada: {project_path}")
    
    result = {"type": "quick", "timestamp": datetime.utcnow().isoformat(), "findings": []}
    
    # Executar secret scanner
    script_dir = Path(__file__).parent
    secret_scanner = script_dir / 'secret_scanner.py'
    
    if secret_scanner.exists():
        try:
            proc = subprocess.run(
                [sys.executable, str(secret_scanner), project_path],
                capture_output=True, text=True, timeout=60
            )
            if proc.stdout:
                # Extrair apenas o JSON final
                lines = proc.stdout.split('\n')
                json_start = next((i for i, l in enumerate(lines) if l.strip().startswith('{')), None)
                if json_start is not None:
                    scan_data = json.loads('\n'.join(lines[json_start:]))
                    result["secrets_found"] = scan_data.get("total_found", 0)
                    result["findings"].extend(scan_data.get("findings", []))
        except Exception as e:
            logger.error(f"Erro no secret scanner: {e}")
    
    result["total_findings"] = len(result["findings"])
    logger.info(f"✅ Varredura rápida concluída: {result['total_findings']} problemas")
    
    return result


def run_full_scan(project_path: str) -> dict:
    """Varredura completa OWASP."""
    logger.info(f"▶ Varredura COMPLETA iniciada: {project_path}")
    
    script_dir = Path(__file__).parent
    scanner = script_dir / 'security_scanner.py'
    
    result = {"type": "full", "timestamp": datetime.utcnow().isoformat()}
    
    if scanner.exists():
        try:
            output_file = f'/tmp/security_scan_{int(time.time())}.json'
            subprocess.run(
                [sys.executable, str(scanner), project_path, '--output', output_file],
                capture_output=True, text=True, timeout=300
            )
            if Path(output_file).exists():
                result.update(json.loads(Path(output_file).read_text()))
                Path(output_file).unlink()
        except Exception as e:
            logger.error(f"Erro no security scanner: {e}")
    
    logger.info(f"✅ Varredura completa: score={result.get('score', '?')}/100, "
                f"problemas={result.get('total_findings', '?')}")
    
    return result


def generate_weekly_report(state: dict, project_path: str):
    """Gera relatório semanal de evolução."""
    logger.info("📊 Gerando relatório semanal...")
    
    history = state.get("scan_history", [])
    full_scans = [s for s in history if s.get("type") == "full"]
    
    if len(full_scans) < 2:
        logger.info("Histórico insuficiente para relatório comparativo.")
        return
    
    first = full_scans[0]
    last  = full_scans[-1]
    
    score_change = last.get("score", 0) - first.get("score", 0)
    
    report_lines = [
        "=" * 50,
        "📊 RELATÓRIO SEMANAL DE SEGURANÇA",
        "=" * 50,
        f"Período: {first.get('timestamp', '?')[:10]} → {last.get('timestamp', '?')[:10]}",
        f"Score inicial: {first.get('score', '?')}/100",
        f"Score atual:   {last.get('score', '?')}/100",
        f"Variação:      {'+' if score_change >= 0 else ''}{score_change} pontos",
        "",
        f"Total de scans realizados: {len(history)}",
        f"Varreduras completas: {len(full_scans)}",
    ]
    
    if score_change > 0:
        report_lines.append("✅ Sua segurança MELHOROU esta semana!")
    elif score_change < 0:
        report_lines.append("⚠️  Sua segurança PIOROU — revise as mudanças recentes.")
    else:
        report_lines.append("➡️  Score estável — continue monitorando.")
    
    report_text = '\n'.join(report_lines)
    logger.info('\n' + report_text)
    
    # Salvar relatório
    report_file = Path(project_path) / f'security_report_{datetime.now().strftime("%Y%m%d")}.txt'
    report_file.write_text(report_text)
    logger.info(f"Relatório salvo em: {report_file}")


# ─── WATCHER DE ARQUIVOS ──────────────────────────────────────────────────────

class FileWatcher(threading.Thread):
    """Monitora mudanças no projeto e dispara rescan."""
    
    def __init__(self, project_path: str, on_change_callback):
        super().__init__(daemon=True)
        self.project_path = project_path
        self.on_change = on_change_callback
        self.running = True
        self.hashes = get_project_hashes(project_path)
        self._pending_rescan = False
        self._last_change = 0
    
    def run(self):
        logger.info(f"👁️  Monitorando mudanças em: {self.project_path}")
        
        while self.running:
            time.sleep(10)  # verifica a cada 10 segundos
            
            new_hashes = get_project_hashes(self.project_path)
            changes = detect_changes(self.hashes, new_hashes)
            
            total_changes = sum(len(v) for v in changes.values())
            
            if total_changes > 0:
                self.hashes = new_hashes
                self._last_change = time.time()
                
                changed_files = changes["modified"] + changes["added"]
                logger.info(f"🔔 {total_changes} arquivo(s) modificado(s): "
                           f"{[Path(f).name for f in changed_files[:3]]}")
                
                # Aguardar estabilização antes de rescanear
                time.sleep(RESCAN_DELAY_AFTER_CHANGE)
                self.on_change(changes)
    
    def stop(self):
        self.running = False


# ─── DAEMON PRINCIPAL ─────────────────────────────────────────────────────────

class SecurityDaemon:
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.state = load_state()
        self.running = True
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        signal.signal(signal.SIGTERM, self._handle_stop)
        signal.signal(signal.SIGINT, self._handle_stop)
    
    def _handle_stop(self, signum, frame):
        logger.info("🛑 Sinal de parada recebido. Encerrando daemon...")
        self.running = False
    
    def _on_file_change(self, changes):
        """Callback quando arquivos são modificados."""
        # Rescan rápido após mudança
        result = run_quick_scan(self.project_path)
        
        if result.get("secrets_found", 0) > 0:
            logger.warning(f"🔴 ALERTA: {result['secrets_found']} secret(s) detectado(s) após mudança!")
            self.state["alerts"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "secret_after_change",
                "count": result["secrets_found"]
            })
        
        self.state["scan_history"].append(result)
        save_state(self.state)
    
    def run(self):
        """Loop principal do daemon."""
        self.state["started_at"] = datetime.utcnow().isoformat()
        save_state(self.state)
        
        # Escrever PID
        Path(PID_FILE).write_text(str(os.getpid()))
        
        logger.info(f"🛡️  Daemon de segurança iniciado (PID: {os.getpid()})")
        logger.info(f"📁 Projeto: {self.project_path}")
        logger.info("📅 Agenda: rápida a cada 6h | completa às 03:00 | relatório semanal")
        
        # Scan inicial
        result = run_full_scan(self.project_path)
        self.state["scan_history"].append(result)
        self.state["last_full_scan"] = datetime.utcnow().isoformat()
        save_state(self.state)
        
        # Iniciar file watcher
        watcher = FileWatcher(self.project_path, self._on_file_change)
        watcher.start()
        
        last_quick = time.time()
        last_full  = time.time()
        start_time = time.time()
        
        while self.running:
            now = time.time()
            current_hour = datetime.now().hour
            
            # Varredura rápida a cada 6 horas
            if now - last_quick >= SCAN_INTERVAL_QUICK:
                result = run_quick_scan(self.project_path)
                self.state["scan_history"].append(result)
                self.state["last_quick_scan"] = datetime.utcnow().isoformat()
                last_quick = now
            
            # Varredura completa diária às 03:00
            if now - last_full >= SCAN_INTERVAL_FULL and current_hour == 3:
                result = run_full_scan(self.project_path)
                self.state["scan_history"].append(result)
                self.state["last_full_scan"] = datetime.utcnow().isoformat()
                last_full = now
                
                # Relatório semanal (domingo = 0)
                if datetime.now().weekday() == 0:
                    generate_weekly_report(self.state, self.project_path)
            
            # Limitar histórico (manter últimos 100 scans)
            if len(self.state["scan_history"]) > 100:
                self.state["scan_history"] = self.state["scan_history"][-100:]
            
            save_state(self.state)
            time.sleep(60)  # verifica agendamento a cada minuto
        
        # Cleanup
        watcher.stop()
        Path(PID_FILE).unlink(missing_ok=True)
        logger.info("👋 Daemon encerrado.")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def cmd_start(project_path: str, daemonize: bool = False):
    daemon = SecurityDaemon(project_path)
    daemon.run()


def cmd_status():
    state = load_state()
    
    pid_running = False
    if Path(PID_FILE).exists():
        pid = int(Path(PID_FILE).read_text())
        try:
            os.kill(pid, 0)
            pid_running = True
        except ProcessLookupError:
            pid_running = False
    
    print("\n🛡️  STATUS DO MONITOR DE SEGURANÇA")
    print("="*40)
    print(f"Status: {'🟢 Rodando' if pid_running else '🔴 Parado'}")
    print(f"Iniciado em: {state.get('started_at', 'N/A')}")
    print(f"Último scan rápido: {state.get('last_quick_scan', 'N/A')}")
    print(f"Último scan completo: {state.get('last_full_scan', 'N/A')}")
    print(f"Total de scans: {len(state.get('scan_history', []))}")
    print(f"Alertas: {len(state.get('alerts', []))}")
    
    history = state.get("scan_history", [])
    if history:
        last = history[-1]
        print(f"\nÚltimo resultado:")
        print(f"  Score: {last.get('score', '?')}/100  {last.get('grade', '')}")
        print(f"  Problemas: {last.get('total_findings', last.get('total_findings', '?'))}")


def cmd_stop():
    if Path(PID_FILE).exists():
        pid = int(Path(PID_FILE).read_text())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"✅ Daemon (PID {pid}) encerrado.")
        except Exception as e:
            print(f"❌ Erro ao parar daemon: {e}")
        Path(PID_FILE).unlink(missing_ok=True)
    else:
        print("⚠️  Daemon não está rodando.")


def cmd_logs(lines: int = 50):
    if Path(LOG_FILE).exists():
        log_lines = Path(LOG_FILE).read_text().splitlines()
        for line in log_lines[-lines:]:
            print(line)
    else:
        print("Sem logs disponíveis.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Security Monitor Daemon')
    parser.add_argument('--project', default='.', help='Caminho do projeto')
    parser.add_argument('--start', action='store_true', help='Iniciar daemon')
    parser.add_argument('--stop', action='store_true', help='Parar daemon')
    parser.add_argument('--status', action='store_true', help='Ver status')
    parser.add_argument('--logs', action='store_true', help='Ver logs recentes')
    parser.add_argument('--lines', type=int, default=50, help='Linhas de log')
    args = parser.parse_args()
    
    if args.start:
        cmd_start(os.path.abspath(args.project))
    elif args.stop:
        cmd_stop()
    elif args.status:
        cmd_status()
    elif args.logs:
        cmd_logs(args.lines)
    else:
        parser.print_help()
