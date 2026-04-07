#!/usr/bin/env python3
"""
security_scanner.py - Varredura OWASP básica.
Compatível com Windows, UTF-8 e saída em JSON.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Finding:
    category: str
    severity: str
    title: str
    file: str
    line: int
    description: str
    recommendation: str

RULES = [
    ('A03 - Injection', 'CRITICA', 'SQL injection via f-string', r'(execute|cursor\.execute)\s*\(\s*f["\']'),
    ('A03 - Injection', 'CRITICA', 'Command injection via shell=True', r'shell\s*=\s*True'),
    ('A02 - Crypto', 'ALTA', 'MD5 usage', r'hashlib\.md5\('),
    ('A05 - Config', 'ALTA', 'CORS wildcard', r'Access-Control-Allow-Origin.*\*|origins\s*=\s*["\']\*["\']'),
    ('A07 - Auth', 'ALTA', 'Hardcoded secret', r'(?i)\b(?:SECRET_KEY|sessionSecret|apiKey|password|senha|accessToken|refreshToken|privateKey)\b\s*=\s*["\'][^"\']{12,}["\']'),
    ('A10 - SSRF', 'ALTA', 'User-controlled URL request', r'requests\.(get|post|put|delete)\s*\(\s*(request\.|params\[|args\[|form\[)'),
]

IGNORED_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build', '.agents'}
SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.php', '.rb', '.go', '.java', '.json', '.yml', '.yaml', '.env', '.txt', '.cfg', '.ini', '.toml'}


def configure_output() -> None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def scan_project(project_path: str) -> list[Finding]:
    path = Path(project_path)
    findings: list[Finding] = []
    if not path.exists():
        return findings

    for file_path in path.rglob('*'):
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        if not file_path.is_file() or file_path.suffix not in SCAN_EXTENSIONS:
            continue
        try:
            lines = file_path.read_text(errors='ignore').splitlines()
        except Exception:
            continue

        for category, severity, title, pattern in RULES:
            for line_no, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(Finding(
                        category=category,
                        severity=severity,
                        title=title,
                        file=str(file_path),
                        line=line_no,
                        description='Pattern matched by security scanner.',
                        recommendation='Review the code path and replace unsafe construction with safe APIs.'
                    ))
                    break

    return findings


def calculate_score(findings: list[Finding]) -> dict:
    score = 100
    for finding in findings:
        score -= {'CRITICA': 20, 'ALTA': 10, 'MEDIA': 5, 'BAIXA': 2}.get(finding.severity, 0)
    score = max(0, score)
    grade = 'Excelente' if score >= 90 else 'Bom' if score >= 80 else 'Regular' if score >= 60 else 'Ruim' if score >= 40 else 'Critico'
    return {'score': score, 'grade': grade}


def print_report(result: dict) -> None:
    print('\n' + '=' * 60)
    print('RELATORIO DE SEGURANCA')
    print('=' * 60)
    print(f"Score: {result['score']}/100  {result['grade']}")
    print(f"Total de problemas: {result['total_findings']}")
    print(f"Criticos: {result['by_severity']['CRITICA']} | Altos: {result['by_severity']['ALTA']} | Medios: {result['by_severity']['MEDIA']} | Baixos: {result['by_severity']['BAIXA']}")

    if not result['findings']:
        print('\nNenhum problema encontrado.')
        return

    severity_labels = {
        'CRITICA': 'CRITICA',
        'ALTA': 'ALTA',
        'MEDIA': 'MEDIA',
        'BAIXA': 'BAIXA',
    }
    print('\nProblemas encontrados:')
    for index, finding in enumerate(result['findings'], 1):
        print(f"\n{index}. [{severity_labels.get(finding['severity'], finding['severity'])}] {finding['category']}")
        print(f"   {finding['title']}")
        print(f"   Local: {finding['file']}:{finding['line']}")
        print(f"   Detalhe: {finding['description']}")
        print(f"   Correção: {finding['recommendation']}")


def main() -> int:
    configure_output()
    parser = argparse.ArgumentParser(description='Security scanner')
    parser.add_argument('project', nargs='?', default='.')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()

    findings = scan_project(args.project)
    score = calculate_score(findings)
    result = {
        'project': args.project,
        'quick': args.quick,
        'score': score['score'],
        'grade': score['grade'],
        'total_findings': len(findings),
        'by_severity': {
            'CRITICA': sum(1 for f in findings if f.severity == 'CRITICA'),
            'ALTA': sum(1 for f in findings if f.severity == 'ALTA'),
            'MEDIA': sum(1 for f in findings if f.severity == 'MEDIA'),
            'BAIXA': sum(1 for f in findings if f.severity == 'BAIXA'),
        },
        'findings': [f.__dict__ for f in findings],
    }

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print_report(result)
    print('\n' + json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
