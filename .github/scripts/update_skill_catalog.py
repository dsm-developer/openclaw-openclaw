from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
MARKER_START = "<!-- SKILL_CATALOG_START -->"
MARKER_END = "<!-- SKILL_CATALOG_END -->"


def read_skill_metadata(skill_dir: Path):
    skill_file = skill_dir / "SKILL.md"
    name = skill_dir.name
    description = ""

    if skill_file.exists():
        text = skill_file.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("Name:"):
                name = line.split(":", 1)[1].strip() or name
            elif line.startswith("Description:"):
                description = line.split(":", 1)[1].strip()

        if not description:
            paragraphs = [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]
            if len(paragraphs) > 0:
                description = paragraphs[0].replace("Name:", "").replace("Description:", "").strip()

    last_updated = get_last_commit_date(skill_file)
    return name, last_updated, description or "No summary available."


def get_last_commit_date(path: Path):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        date_text = result.stdout.strip()
        if date_text:
            return date_text
    except subprocess.CalledProcessError:
        pass
    return path.stat().st_mtime


def build_catalog():
    if not SKILLS_DIR.exists():
        return []

    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        if skill_dir.name == "_template":
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        skills.append(read_skill_metadata(skill_dir))

    return skills


def render_table(skills):
    lines = [
        "| Skill Name | Last Updated | AI Capability Summary |",
        "|---|---|---|",
    ]
    for name, last_updated, summary in skills:
        summary_clean = summary.replace("|", "\u2014")
        lines.append(f"| {name} | {last_updated} | {summary_clean} |")
    return "\n".join(lines)


def update_readme():
    content = README.read_text(encoding="utf-8")
    if MARKER_START not in content or MARKER_END not in content:
        raise RuntimeError("README markers not found")

    before, rest = content.split(MARKER_START, 1)
    _, after = rest.split(MARKER_END, 1)
    skills = build_catalog()
    if not skills:
        table_block = "| Skill Name | Last Updated | AI Capability Summary |\n|---|---|---|\n| _No skills detected yet. Run the workflow to populate this table._ | | |"
    else:
        table_block = render_table(skills)

    new_content = before + MARKER_START + "\n" + table_block + "\n" + MARKER_END + after
    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
