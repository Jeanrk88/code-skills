#!/usr/bin/env python3
"""
stack_detector.py - Detecta a stack do projeto.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def configure_output() -> None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def detect_stack(project_path: str) -> dict:
    path = Path(project_path)
    result = {
        'backend': 'unknown',
        'frontend': 'none',
        'database': 'none',
        'auth': 'none',
        'hosting': 'unknown',
        'frameworks': [],
        'entry_points': [],
        'risk_summary': [],
    }
    if not path.exists():
        return {'error': f'Directory not found: {project_path}'}

    files = [f for f in path.rglob('*') if f.is_file() and not any(part in {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build'} for part in f.parts)]
    names = [f.name for f in files]
    content = ''
    for f in files[:50]:
        try:
            content += f.read_text(errors='ignore')
        except Exception:
            pass

    if 'package.json' in names:
        result['backend'] = 'node'
        try:
            pkg = json.loads((path / 'package.json').read_text(encoding='utf-8'))
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
            if 'vue' in deps:
                result['frontend'] = 'vue'
                result['frameworks'].append('Vue')
            if 'react' in deps:
                result['frontend'] = 'react'
                result['frameworks'].append('React')
            if 'nuxt' in deps:
                result['frameworks'].append('Nuxt')
        except Exception:
            pass

    if any(f.suffix == '.py' for f in files):
        result['backend'] = 'python'
        result['frameworks'].append('Python')

    if any(f.suffix == '.php' for f in files):
        result['backend'] = 'php'

    if re.search(r'postgres|psycopg2|postgres://', content, re.IGNORECASE):
        result['database'] = 'postgres'
    elif re.search(r'mysql|mysql://', content, re.IGNORECASE):
        result['database'] = 'mysql'
    elif re.search(r'sqlite|sqlite:///', content, re.IGNORECASE):
        result['database'] = 'sqlite'

    if re.search(r'jwt|jsonwebtoken|pyjwt', content, re.IGNORECASE):
        result['auth'] = 'jwt'
    elif re.search(r'session|express-session|flask_login', content, re.IGNORECASE):
        result['auth'] = 'session'

    if 'vercel.json' in names:
        result['hosting'] = 'vercel'
    elif 'Dockerfile' in names:
        result['hosting'] = 'docker'

    result['entry_points'] = [name for name in ['app.py', 'main.py', 'server.py', 'index.js', 'index.ts', 'nuxt.config.ts'] if name in names]
    if (path / '.env').exists():
        result['risk_summary'].append('Arquivo .env encontrado')
    if not result['frameworks']:
        result['frameworks'].append('not detected')
    return result


def print_report(result: dict) -> None:
    print('\n' + '=' * 60)
    print('RECONHECIMENTO DE STACK')
    print('=' * 60)
    if 'error' in result:
        print(result['error'])
        return

    print(f"Backend: {result['backend']}")
    print(f"Frontend: {result['frontend']}")
    print(f"Banco: {result['database']}")
    print(f"Auth: {result['auth']}")
    print(f"Hosting: {result['hosting']}")
    print(f"Frameworks: {', '.join(result['frameworks'])}")
    print(f"Entry points: {', '.join(result['entry_points']) or 'nenhum detectado'}")
    if result['risk_summary']:
        print('Alertas:')
        for item in result['risk_summary']:
            print(f" - {item}")


def main() -> int:
    configure_output()
    parser = argparse.ArgumentParser(description='Stack detector')
    parser.add_argument('project', nargs='?', default='.')
    args = parser.parse_args()
    result = detect_stack(args.project)
    print_report(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
