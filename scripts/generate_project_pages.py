#!/usr/bin/env python3

from __future__ import annotations

from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "_projects"
OUTPUT_DIR = ROOT / "projects"
INDEX_FILE = ROOT / "index.html"
IMAGE_PATTERN = re.compile(r'^!\[(?P<alt>[^\]]*)\]\((?P<src>\S+)(?:\s+"(?P<title>[^"]*)")?\)$')
INDEX_CARDS_START = "<!-- generated:project-cards:start -->"
INDEX_CARDS_END = "<!-- generated:project-cards:end -->"
ASSET_VERSION = "20260626-1"


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


def split_bilingual_body(markdown: str) -> dict[str, str]:
    marker_en = "<!-- lang:en -->"
    marker_ru = "<!-- lang:ru -->"

    if marker_en not in markdown or marker_ru not in markdown:
        return {"en": markdown.strip(), "ru": markdown.strip()}

    after_en = markdown.split(marker_en, 1)[1]
    en_body, ru_body = after_en.split(marker_ru, 1)
    return {"en": en_body.strip(), "ru": ru_body.strip()}


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

        image_match = IMAGE_PATTERN.match(line)
        if image_match:
            flush_paragraph()
            flush_list()
            alt_text = escape(image_match.group("alt") or "")
            src_value = escape(image_match.group("src") or "")
            title_value = image_match.group("title")
            title_attr = f' title="{escape(title_value)}"' if title_value else ""
            parts.append(
                f'<img src="{src_value}" alt="{alt_text}" loading="lazy"{title_attr}>'
            )
            continue

        flush_list()
        paragraph.append(line)

    flush_paragraph()
    flush_list()
    return "\n          ".join(parts)


def asset_path(path: str) -> str:
    trimmed = path.lstrip("/")
    return f"../../{trimmed}"


def home_asset_path(path: str) -> str:
    return path.lstrip("/")


def get_text(data: dict[str, object], key: str, language: str) -> str:
    localized_key = f"{key}_ru" if language == "ru" else key
    fallback_key = key if language == "ru" else f"{key}_ru"
    return str(data.get(localized_key) or data.get(fallback_key) or "")


def get_tags(data: dict[str, object], language: str) -> list[str]:
    localized_key = "tags_ru" if language == "ru" else "tags"
    fallback_key = "tags" if language == "ru" else "tags_ru"
    localized_tags = data.get(localized_key) or data.get(fallback_key) or []
    return [str(tag) for tag in localized_tags if isinstance(tag, str)]


def render_tag_html(tags_en: list[str], tags_ru: list[str]) -> str:
    tag_count = max(len(tags_en), len(tags_ru))
    items: list[str] = []

    for index in range(tag_count):
        en_tag = escape(tags_en[index] if index < len(tags_en) else tags_ru[index])
        ru_tag = escape(tags_ru[index] if index < len(tags_ru) else tags_en[index])
        items.append(
            f'\n              <span data-i18n-en="{en_tag}" data-i18n-ru="{ru_tag}">{en_tag}</span>'
        )

    return "".join(items)


def render_home_card(data: dict[str, object], slug: str) -> str:
    title_en = escape(get_text(data, "title", "en"))
    title_ru = escape(get_text(data, "title", "ru"))
    description_en = escape(get_text(data, "description", "en"))
    description_ru = escape(get_text(data, "description", "ru"))
    github = escape(str(data["github"]))
    image = escape(home_asset_path(str(data["image"])))
    href = f"projects/{escape(slug)}/"
    tags_en = get_tags(data, "en")
    tags_ru = get_tags(data, "ru")
    tag_html = render_tag_html(tags_en, tags_ru)

    return f"""          <article class="project-card">
            <a
              href="{href}"
              aria-label="Open {title_en} project page"
              data-i18n-aria-label-en="Open {title_en} project page"
              data-i18n-aria-label-ru="Открыть страницу проекта {title_ru}"
            >
              <img
                class="project-image"
                src="{image}"
                alt="{title_en} preview"
                data-i18n-alt-en="{title_en} preview"
                data-i18n-alt-ru="Превью проекта {title_ru}"
              >
            </a>
            <div class="project-body">
              <h3><a href="{href}" data-i18n-en="{title_en}" data-i18n-ru="{title_ru}">{title_en}</a></h3>
              <div
                class="tag-list"
                aria-label="{title_en} tags"
                data-i18n-aria-label-en="{title_en} tags"
                data-i18n-aria-label-ru="Теги проекта {title_ru}"
              >{tag_html}
              </div>
              <p data-i18n-en="{description_en}" data-i18n-ru="{description_ru}">{description_en}</p>
              <a
                class="project-link"
                href="{github}"
                target="_blank"
                rel="noreferrer"
                data-i18n-en="GitHub repository"
                data-i18n-ru="Репозиторий GitHub"
              >GitHub repository</a>
            </div>
          </article>"""


def replace_generated_cards(index_html: str, cards_html: str) -> str:
    pattern = re.compile(
        rf"(?P<before>{re.escape(INDEX_CARDS_START)}\n)(?P<body>.*?)(?P<after>\n\s*{re.escape(INDEX_CARDS_END)})",
        re.DOTALL,
    )
    match = pattern.search(index_html)
    if not match:
        raise ValueError("Could not find generated project cards block in index.html")

    return (
        index_html[: match.start("before")]
        + match.group("before")
        + cards_html
        + match.group("after")
        + index_html[match.end("after") :]
    )


def render_project_page(data: dict[str, object], bodies: dict[str, str]) -> str:
    title_en = escape(get_text(data, "title", "en"))
    title_ru = escape(get_text(data, "title", "ru"))
    description_en = escape(get_text(data, "description", "en"))
    description_ru = escape(get_text(data, "description", "ru"))
    image = asset_path(str(data["image"]))
    github = escape(str(data["github"]))
    tags_en = get_tags(data, "en")
    tags_ru = get_tags(data, "ru")
    tag_html = render_tag_html(tags_en, tags_ru)
    body_en = render_markdown(bodies["en"])
    body_ru = render_markdown(bodies["ru"])

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{description_en}">
    <title>{title_en} | Yedil Sarseke</title>
    <link rel="stylesheet" href="../../assets/styles.css?v={ASSET_VERSION}">
  </head>
  <body
    data-page-title-en="{title_en} | Yedil Sarseke"
    data-page-title-ru="{title_ru} | Yedil Sarseke"
    data-page-description-en="{description_en}"
    data-page-description-ru="{description_ru}"
  >
    <header class="site-header">
      <a
        class="brand"
        href="../../index.html#home"
        aria-label="Portfolio home"
        data-i18n-aria-label-en="Portfolio home"
        data-i18n-aria-label-ru="Главная страница портфолио"
      >
        <span class="brand-name" data-profile="name">Engineer</span>
      </a>
      <div class="header-controls">
        <nav
          class="site-nav"
          aria-label="Primary navigation"
          data-i18n-aria-label-en="Primary navigation"
          data-i18n-aria-label-ru="Основная навигация"
        >
          <a href="../../index.html#experience" data-i18n-en="Experience" data-i18n-ru="Опыт">Experience</a>
          <a href="../../index.html#projects" data-i18n-en="Projects" data-i18n-ru="Проекты">Projects</a>
          <a href="../../index.html#skills" data-i18n-en="Skills" data-i18n-ru="Навыки">Skills</a>
          <a href="../../index.html#contact" data-i18n-en="Contact" data-i18n-ru="Контакты">Contact</a>
        </nav>
        <label class="language-switcher">
          <span class="sr-only" data-i18n-en="Language" data-i18n-ru="Язык">Language</span>
          <select
            class="language-select"
            data-language-select
            aria-label="Language"
            data-i18n-aria-label-en="Language"
            data-i18n-aria-label-ru="Язык"
          >
            <option value="en">EN</option>
            <option value="ru">RU</option>
          </select>
        </label>
      </div>
    </header>

    <main>
      <section class="project-detail section-wrap">
        <a
          class="back-link"
          href="../../index.html#projects"
          data-i18n-en="Back to projects"
          data-i18n-ru="Назад к проектам"
        >Back to projects</a>
        <div class="project-detail-grid">
          <div>
            <p class="eyebrow" data-i18n-en="Project" data-i18n-ru="Проект">Project</p>
            <h1 data-i18n-en="{title_en}" data-i18n-ru="{title_ru}">{title_en}</h1>
            <div
              class="tag-list large"
              aria-label="{title_en} tags"
              data-i18n-aria-label-en="{title_en} tags"
              data-i18n-aria-label-ru="Теги проекта {title_ru}"
            >{tag_html}
            </div>
            <p class="lead" data-i18n-en="{description_en}" data-i18n-ru="{description_ru}">{description_en}</p>
            <div class="hero-actions">
              <a class="button primary" href="{github}" target="_blank" rel="noreferrer" data-i18n-en="GitHub Repository" data-i18n-ru="Репозиторий GitHub">GitHub Repository</a>
              <a class="button secondary" href="../../index.html#contact" data-i18n-en="Contact Me" data-i18n-ru="Связаться со мной">Contact Me</a>
            </div>
          </div>
          <img
            class="project-detail-image"
            src="{image}"
            alt="{title_en} preview"
            data-i18n-alt-en="{title_en} preview"
            data-i18n-alt-ru="Превью проекта {title_ru}"
          >
        </div>
        <article class="project-notes markdown-content">
          <div data-lang-content="en">
            {body_en}
          </div>
          <div data-lang-content="ru" hidden>
            {body_ru}
          </div>
        </article>
      </section>
    </main>

    <script src="../../assets/site.js?v={ASSET_VERSION}"></script>
  </body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    project_entries: list[tuple[int, str, dict[str, object], str]] = []

    for project_path in sorted(PROJECTS_DIR.glob("*.md")):
        data, body = parse_project_file(project_path)
        slug = project_path.stem
        order = int(str(data.get("order", "999")))
        project_entries.append((order, slug, data, body))

    project_entries.sort(key=lambda entry: (entry[0], entry[1]))

    for _, slug, data, body in project_entries:
        page_dir = OUTPUT_DIR / slug
        page_dir.mkdir(parents=True, exist_ok=True)

        html = render_project_page(data, split_bilingual_body(body))
        (page_dir / "index.html").write_text(html, encoding="utf-8")

    cards_html = "\n\n".join(render_home_card(data, slug) for _, slug, data, _ in project_entries)
    index_html = INDEX_FILE.read_text(encoding="utf-8")
    updated_index = replace_generated_cards(index_html, cards_html)
    INDEX_FILE.write_text(updated_index, encoding="utf-8")


if __name__ == "__main__":
    main()
