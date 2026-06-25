#!/usr/bin/env python3

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "_projects"
OUTPUT_DIR = ROOT / "projects"


def parse_project_file(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError(f"{path} is missing front matter")

    frontmatter: dict[str, object] = {}
    index = 1

    while index < len(lines):
        line = lines[index]
        index += 1

        if line.strip() == "---":
            break

        if not line.strip():
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        if value:
            frontmatter[key] = value
            continue

        items: list[str] = []
        while index < len(lines):
            next_line = lines[index]
            stripped = next_line.strip()
            if stripped.startswith("- "):
                items.append(stripped[2:].strip())
                index += 1
                continue
            if not stripped:
                index += 1
                continue
            break
        frontmatter[key] = items

    body = "\n".join(lines[index:]).strip()
    return frontmatter, body


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            content = " ".join(item.strip() for item in paragraph)
            parts.append(f"<p>{escape(content)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            items_html = "".join(f"<li>{escape(item)}</li>" for item in list_items)
            parts.append(f"<ul>{items_html}</ul>")
            list_items = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            flush_paragraph()
            flush_list()
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            parts.append(f"<h3>{escape(line[4:].strip())}</h3>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            parts.append(f"<h2>{escape(line[3:].strip())}</h2>")
            continue

        if line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
            continue

        flush_list()
        paragraph.append(line)

    flush_paragraph()
    flush_list()
    return "\n          ".join(parts)


def asset_path(path: str) -> str:
    trimmed = path.lstrip("/")
    return f"../../{trimmed}"


def render_project_page(data: dict[str, object], body_html: str) -> str:
    title = str(data["title"])
    description = str(data["description"])
    image = asset_path(str(data["image"]))
    github = str(data["github"])
    tags = data.get("tags", [])
    tag_html = "".join(f"\n              <span>{escape(tag)}</span>" for tag in tags if isinstance(tag, str))

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{escape(description)}">
    <title>{escape(title)} | Yedil Sarseke</title>
    <link rel="stylesheet" href="../../assets/styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="../../index.html#home" aria-label="Portfolio home">
        <span class="brand-mark">ENG</span>
        <span class="brand-name" data-profile="name">Engineer</span>
      </a>
      <nav class="site-nav" aria-label="Primary navigation">
        <a href="../../index.html#experience">Experience</a>
        <a href="../../index.html#projects">Projects</a>
        <a href="../../index.html#skills">Skills</a>
        <a href="../../index.html#contact">Contact</a>
      </nav>
    </header>

    <main>
      <section class="project-detail section-wrap">
        <a class="back-link" href="../../index.html#projects">Back to projects</a>
        <div class="project-detail-grid">
          <div>
            <p class="eyebrow">Project</p>
            <h1>{escape(title)}</h1>
            <div class="tag-list large" aria-label="{escape(title)} tags">{tag_html}
            </div>
            <p class="lead">{escape(description)}</p>
            <div class="hero-actions">
              <a class="button primary" href="{escape(github)}" target="_blank" rel="noreferrer">GitHub Repository</a>
              <a class="button secondary" href="../../index.html#contact">Contact Me</a>
            </div>
          </div>
          <img class="project-detail-image" src="{image}" alt="{escape(title)} preview">
        </div>
        <article class="project-notes markdown-content">
          {body_html}
        </article>
      </section>
    </main>

    <script src="../../assets/site.js"></script>
  </body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    for project_path in sorted(PROJECTS_DIR.glob("*.md")):
        data, body = parse_project_file(project_path)
        slug = project_path.stem
        page_dir = OUTPUT_DIR / slug
        page_dir.mkdir(parents=True, exist_ok=True)

        html = render_project_page(data, render_markdown(body))
        (page_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
