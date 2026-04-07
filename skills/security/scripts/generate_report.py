#!/usr/bin/env python3
"""
generate_report.py — Gera relatório HTML completo com score, gráficos e checklist.
Uso: python generate_report.py --project /caminho/do/projeto --output relatorio.html
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def load_scan_history() -> list:
    """Carrega histórico de scans do monitor."""
    state_file = Path('/tmp/security_monitor_state.json')
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text())
            return [s for s in state.get('scan_history', []) if 'score' in s]
        except Exception:
            pass
    return []


def run_scan(project_path: str) -> dict:
    """Executa scan se não houver dados recentes."""
    import subprocess
    script_dir = Path(__file__).parent
    scanner = script_dir / 'security_scanner.py'
    
    if scanner.exists():
        output_file = '/tmp/report_scan.json'
        subprocess.run(
            [sys.executable, str(scanner), project_path, '--output', output_file],
            capture_output=True, text=True, timeout=300
        )
        if Path(output_file).exists():
            data = json.loads(Path(output_file).read_text())
            Path(output_file).unlink()
            return data
    
    return {"score": 0, "grade": "N/A", "total_findings": 0, "findings": [], "by_severity": {}}


def generate_html_report(scan_data: dict, history: list, project_path: str) -> str:
    """Gera o HTML completo do relatório."""
    
    findings = scan_data.get('findings', [])
    score = scan_data.get('score', 0)
    grade = scan_data.get('grade', 'N/A')
    sev = scan_data.get('by_severity', {})
    
    # Dados do gráfico histórico
    chart_labels = []
    chart_scores = []
    for s in history[-20:]:  # últimos 20 scans
        chart_labels.append(s.get('timestamp', '')[:10])
        chart_scores.append(s.get('score', 0))
    
    if not chart_scores:
        chart_labels = [datetime.now().strftime('%Y-%m-%d')]
        chart_scores = [score]
    
    # Cor do score
    if score >= 90:
        score_color = '#10b981'  # verde
    elif score >= 80:
        score_color = '#34d399'
    elif score >= 60:
        score_color = '#f59e0b'  # amarelo
    elif score >= 40:
        score_color = '#f97316'  # laranja
    else:
        score_color = '#ef4444'  # vermelho
    
    # Checklist de proteções
    checklist_items = [
        ("Headers de segurança HTTP", not any('header' in f.get('title','').lower() for f in findings)),
        ("Proteção CSRF", not any('csrf' in f.get('title','').lower() for f in findings)),
        ("Rate limiting ativo", not any('rate limit' in f.get('title','').lower() for f in findings)),
        ("Hashing seguro de senhas", not any('md5' in f.get('title','').lower() or 'sha1' in f.get('title','').lower() for f in findings)),
        ("Sem SQL Injection", not any('sql' in f.get('title','').lower() for f in findings)),
        ("Sem XSS detectado", not any('xss' in f.get('title','').lower() for f in findings)),
        ("Sem secrets expostos", not any('secret' in f.get('title','').lower() or 'hardcoded' in f.get('title','').lower() for f in findings)),
        ("Sem DEBUG em produção", not any('debug' in f.get('title','').lower() for f in findings)),
        ("Sem Command Injection", not any('command' in f.get('title','').lower() for f in findings)),
        ("Sem deserialização insegura", not any('pickle' in f.get('title','').lower() for f in findings)),
    ]
    
    checklist_html = ''
    for label, ok in checklist_items:
        icon = '✅' if ok else '❌'
        color = '#10b981' if ok else '#ef4444'
        checklist_html += f'<div class="check-item"><span style="color:{color}">{icon}</span> {label}</div>\n'
    
    # Findings HTML
    findings_html = ''
    sev_colors = {'CRÍTICA': '#ef4444', 'ALTA': '#f97316', 'MÉDIA': '#f59e0b', 'BAIXA': '#10b981'}
    sev_icons  = {'CRÍTICA': '🔴', 'ALTA': '🟠', 'MÉDIA': '🟡', 'BAIXA': '🟢'}
    
    for f in findings:
        color = sev_colors.get(f.get('severity',''), '#6b7280')
        icon  = sev_icons.get(f.get('severity',''), '⚪')
        snippet = f.get('code_snippet', '')
        snippet_html = f'<div class="code-snippet"><code>{snippet}</code></div>' if snippet else ''
        
        findings_html += f'''
        <div class="finding">
            <div class="finding-header" style="border-left: 4px solid {color}">
                <span class="severity-badge" style="background:{color}">{icon} {f.get('severity','')}</span>
                <span class="finding-title">{f.get('title','')}</span>
                <span class="finding-category">{f.get('category','')}</span>
            </div>
            <div class="finding-body">
                <div class="finding-location">📁 {f.get('file','')}:{f.get('line','')}</div>
                <div class="finding-desc">💬 {f.get('description','')}</div>
                <div class="finding-fix">✅ {f.get('recommendation','')}</div>
                {snippet_html}
            </div>
        </div>'''
    
    if not findings_html:
        findings_html = '<div class="no-findings">✅ Nenhum problema crítico encontrado!</div>'
    
    # Dados do gráfico
    chart_data = json.dumps(chart_scores)
    chart_labels_js = json.dumps(chart_labels)
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório de Segurança — {Path(project_path).name}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
  
  /* Header */
  .header {{ text-align: center; padding: 3rem 0; border-bottom: 1px solid #1e293b; }}
  .header h1 {{ font-size: 2.5rem; font-weight: 700; color: #f1f5f9; }}
  .header .subtitle {{ color: #94a3b8; margin-top: 0.5rem; }}
  .header .timestamp {{ color: #64748b; font-size: 0.875rem; margin-top: 0.5rem; }}
  
  /* Score */
  .score-section {{ display: flex; justify-content: center; padding: 3rem 0; }}
  .score-card {{ text-align: center; background: #1e293b; border-radius: 1.5rem; padding: 3rem 4rem; }}
  .score-number {{ font-size: 5rem; font-weight: 800; color: {score_color}; line-height: 1; }}
  .score-max {{ font-size: 1.5rem; color: #64748b; }}
  .score-grade {{ font-size: 1.5rem; margin-top: 1rem; color: {score_color}; }}
  
  /* Stats grid */
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }}
  .stat {{ background: #1e293b; border-radius: 0.75rem; padding: 1.5rem; text-align: center; }}
  .stat-number {{ font-size: 2.5rem; font-weight: 700; }}
  .stat-label {{ color: #94a3b8; font-size: 0.875rem; margin-top: 0.25rem; }}
  .stat-critica {{ color: #ef4444; }}
  .stat-alta {{ color: #f97316; }}
  .stat-media {{ color: #f59e0b; }}
  .stat-baixa {{ color: #10b981; }}
  
  /* Sections */
  .section {{ margin: 3rem 0; }}
  .section h2 {{ font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1.5rem;
                 padding-bottom: 0.75rem; border-bottom: 2px solid #1e293b; }}
  
  /* Chart */
  .chart-container {{ background: #1e293b; border-radius: 0.75rem; padding: 1.5rem; }}
  
  /* Checklist */
  .checklist {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 0.75rem; }}
  .check-item {{ background: #1e293b; padding: 0.75rem 1rem; border-radius: 0.5rem; font-size: 0.9rem; }}
  
  /* Findings */
  .finding {{ background: #1e293b; border-radius: 0.75rem; margin-bottom: 1rem; overflow: hidden; }}
  .finding-header {{ padding: 1rem 1.25rem; display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }}
  .severity-badge {{ padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; color: white; }}
  .finding-title {{ font-weight: 600; flex: 1; }}
  .finding-category {{ color: #64748b; font-size: 0.8rem; }}
  .finding-body {{ padding: 0 1.25rem 1.25rem; }}
  .finding-location {{ color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem; }}
  .finding-desc {{ color: #cbd5e1; margin-bottom: 0.5rem; font-size: 0.9rem; }}
  .finding-fix {{ color: #86efac; font-size: 0.9rem; }}
  .code-snippet {{ background: #0f172a; padding: 0.75rem; border-radius: 0.5rem; margin-top: 0.75rem;
                   font-family: monospace; font-size: 0.8rem; color: #f8d57e; overflow-x: auto; }}
  .no-findings {{ background: #1e293b; border-radius: 0.75rem; padding: 2rem; text-align: center;
                  color: #10b981; font-size: 1.1rem; }}
  
  /* Footer */
  footer {{ text-align: center; color: #475569; padding: 2rem; margin-top: 3rem;
             border-top: 1px solid #1e293b; font-size: 0.875rem; }}
</style>
</head>
<body>
<div class="container">
  
  <div class="header">
    <h1>🔐 Relatório de Segurança</h1>
    <div class="subtitle">Projeto: <strong>{Path(project_path).name}</strong></div>
    <div class="timestamp">Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>
  </div>
  
  <div class="score-section">
    <div class="score-card">
      <div class="score-number">{score}<span class="score-max">/100</span></div>
      <div class="score-grade">{grade}</div>
    </div>
  </div>
  
  <div class="stats">
    <div class="stat">
      <div class="stat-number stat-critica">{sev.get('CRÍTICA', 0)}</div>
      <div class="stat-label">🔴 Críticos</div>
    </div>
    <div class="stat">
      <div class="stat-number stat-alta">{sev.get('ALTA', 0)}</div>
      <div class="stat-label">🟠 Altos</div>
    </div>
    <div class="stat">
      <div class="stat-number stat-media">{sev.get('MÉDIA', 0)}</div>
      <div class="stat-label">🟡 Médios</div>
    </div>
    <div class="stat">
      <div class="stat-number stat-baixa">{sev.get('BAIXA', 0)}</div>
      <div class="stat-label">🟢 Baixos</div>
    </div>
  </div>
  
  <div class="section">
    <h2>📈 Evolução do Score</h2>
    <div class="chart-container">
      <canvas id="scoreChart"></canvas>
    </div>
  </div>
  
  <div class="section">
    <h2>✅ Checklist de Proteções</h2>
    <div class="checklist">
      {checklist_html}
    </div>
  </div>
  
  <div class="section">
    <h2>🚨 Problemas Encontrados ({scan_data.get('total_findings', 0)})</h2>
    {findings_html}
  </div>
  
  <footer>
    Gerado pela Security Skill • Proteja seu código, proteja seus usuários 🛡️
  </footer>
  
</div>
<script>
const ctx = document.getElementById('scoreChart').getContext('2d');
new Chart(ctx, {{
  type: 'line',
  data: {{
    labels: {chart_labels_js},
    datasets: [{{
      label: 'Score de Segurança',
      data: {chart_data},
      borderColor: '{score_color}',
      backgroundColor: '{score_color}22',
      tension: 0.4,
      fill: true,
      pointBackgroundColor: '{score_color}',
      pointRadius: 5,
    }}]
  }},
  options: {{
    responsive: true,
    scales: {{
      y: {{ min: 0, max: 100, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
      x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }}
    }},
    plugins: {{
      legend: {{ labels: {{ color: '#e2e8f0' }} }},
      tooltip: {{ callbacks: {{ label: ctx => `Score: ${{ctx.raw}}/100` }} }}
    }}
  }}
}});
</script>
</body>
</html>'''
    
    return html


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', default='.', help='Caminho do projeto')
    parser.add_argument('--output', default='relatorio_seguranca.html', help='Arquivo de saída')
    args = parser.parse_args()
    
    project = os.path.abspath(args.project)
    
    print("🔍 Executando scan para o relatório...")
    scan_data = run_scan(project)
    
    print("📊 Carregando histórico...")
    history = load_scan_history()
    history.append(scan_data)
    
    print("📝 Gerando relatório HTML...")
    html = generate_html_report(scan_data, history, project)
    
    output_path = Path(args.output)
    output_path.write_text(html, encoding='utf-8')
    
    print(f"\n✅ Relatório gerado: {output_path.absolute()}")
    print(f"📊 Score: {scan_data.get('score', 0)}/100  {scan_data.get('grade', '')}")
    print(f"🚨 Problemas: {scan_data.get('total_findings', 0)}")
    print(f"\n💡 Abra o arquivo no navegador para visualizar o relatório completo.")