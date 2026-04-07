#!/usr/bin/env python3
"""
secret_scanner.py - Encontra secrets e credenciais expostas.
Compatível com Windows, UTF-8 e log configurável.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_LOG_DIR = Path(os.environ.get('SECURITY_SKILL_LOG_DIR') or (Path(tempfile.gettempdir()) / 'security_skill_logs'))
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / 'security_monitor.log'

SECRET_PATTERNS = {
    'OpenAI API Key': r'sk-[a-zA-Z0-9]{48}',
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'Stripe Secret Key': r'sk_live_[0-9a-zA-Z]{24}',
    'Generic Password': r'(password|senha|pass|pwd)\s*=\s*["\'][^"\']{4,}["\']',
    'Generic API Key': r'(api_key|apikey|api-key)\s*=\s*["\'][^"\']{8,}["\']',
    'JWT Token': r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
    'Private Key': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
    'Database URL': r'(postgres|mysql|mongodb):\/\/[^\s"\']+:[^\s"\']+@',
    'GitHub Token': r'ghp_[a-zA-Z0-9]{36}',
    'Slack Token': r'xox[baprs]-[0-9a-zA-Z-]{10,}',
}

IGNORED_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build', '.agents'}
SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.php', '.rb', '.go', '.java', '.json', '.yml', '.yaml', '.env', '.txt', '.cfg', '.ini', '.toml'}


def configure_output() -> None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def setup_logger() -> logging.Logger:
    DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger('secret_scanner')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(DEFAULT_LOG_FILE, encoding='utf-8')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def scan_file(file_path: Path) -> list[dict]:
    findings: list[dict] = []
    try:
        content = file_path.read_text(errors='ignore')
    except Exception:
        return findings

    for label, pattern in SECRET_PATTERNS.items():
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line = content.count('\n', 0, match.start()) + 1
            findings.append({
                'type': label,
                'file': str(file_path),
                'line': line,
                'match': match.group(0)[:120],
            })
    return findings


def scan_project(project_path: str) -> dict:
    path = Path(project_path)
    findings: list[dict] = []
    if not path.exists():
        return {'error': f'Directory not found: {project_path}', 'findings': [], 'total_found': 0}

    for file_path in path.rglob('*'):
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        if not file_path.is_file() or file_path.suffix not in SCAN_EXTENSIONS:
            continue
        findings.extend(scan_file(file_path))

    return {
        'ok': True,
        'project': str(path),
        'total_found': len(findings),
        'findings': findings,
    }


def print_report(result: dict) -> None:
    print('\n' + '=' * 60)
    print('RELATORIO DE SECRETS')
    print('=' * 60)
    if 'error' in result:
        print(result['error'])
        return

    print(f"Total de secrets encontrados: {result['total_found']}")
    if not result['findings']:
        print('Nenhum secret exposto encontrado.')
        return

    for index, finding in enumerate(result['findings'], 1):
        print(f"\n{index}. {finding['type']}")
        print(f"   Local: {finding['file']}:{finding['line']}")
        print(f"   Match: {finding['match']}")


def main() -> int:
    configure_output()
    logger = setup_logger()

    parser = argparse.ArgumentParser(description='Secret scanner')
    parser.add_argument('project', nargs='?', default='.')
    args = parser.parse_args()

    result = scan_project(args.project)
    if 'error' in result:
        logger.error(result['error'])
    else:
        logger.info('Secret scan completed: %s findings', result['total_found'])

    print_report(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
