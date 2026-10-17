#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
for skill in skills:
    text = skill.read_text()
    header = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not header:
        errors.append(f"{skill.relative_to(ROOT)}: missing frontmatter")
        continue
    fields = dict(re.findall(r"^([\w-]+):\s*(.*)$", header[1], re.M))
    if fields.get("name", "").strip('\"\'') != skill.parent.name:
        errors.append(f"{skill.relative_to(ROOT)}: name must match directory")
    if not fields.get("description"):
        errors.append(f"{skill.relative_to(ROOT)}: missing description")
    for field in ["icon", "color", "mode", "reminder"]:
        if field in fields:
            errors.append(f"{skill.relative_to(ROOT)}: unsupported field {field}")
    if "p3-models.md" in text and skill.parent.name != "setup-p3" and "~/.agents/p3-models.md" not in text:
        errors.append(f"{skill.relative_to(ROOT)}: missing global model fallback")

for file in [*(ROOT / "skills").rglob("*.md"), *(ROOT / "agents").rglob("*.md")]:
    text = file.read_text()
    for pattern in [r"^<<<<<<< ", r"^>>>>>>> ", r"\bCursor\b", r"\bTask tool\b", r"subagent_type", r"\.cursor/", r"agent-transcripts", r"AskQuestion", r"/loop\b", r"cursor-team-kit", r"(?:claude-opus|grok-\d|gpt-\d)"]:
        if re.search(pattern, text, re.M):
            errors.append(f"{file.relative_to(ROOT)}: unported mechanism {pattern}")
    for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
        target = link.split("#", 1)[0]
        if not target or re.match(r"[a-z][a-z0-9+.-]*:", target) or any(c in target for c in "<>*"):
            continue
        if not (file.parent / target).exists():
            errors.append(f"{file.relative_to(ROOT)}: broken link {target}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"Verified {len(skills)} skills: metadata, local links, model fallback, and T3 mechanisms.")
