import json
from pathlib import Path

from .security_scanner import scan_project


def test_form_step_mentions_is_not_flagged(tmp_path: Path):
    file_path = tmp_path / 'form-step-mentions.ts'
    file_path.write_text(
        "export const FIRST_NAME_MENTION_TOKEN = '@nome_proprio'\n",
        encoding='utf-8',
    )

    findings = scan_project(str(tmp_path))
    assert all('form-step-mentions.ts' not in finding.file for finding in findings)
