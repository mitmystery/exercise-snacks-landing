#!/usr/bin/env python3
"""Generate entitymap.html from entitymap.json.

entitymap.html is derived, never hand-edited: edit entitymap.json and re-run
this. Hand edits are lost on the next run, which is the point — the two files
drifting apart is what this replaced.

    python3 tools/generate-entitymap-html.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = "https://apps.apple.com/gb/app/exercise-snacks-desk-breaks/id6759562504"
e = html.escape

NAV = f"""  <nav class="site-nav">
    <div class="container site-nav-inner">
      <a class="site-nav-brand" href="/">Exercise Snacks</a>
      <div class="site-nav-links">
        <a href="/guides/">Guides</a>
        <a class="nav-hide-sm" href="/#research">Research</a>
        <a class="btn btn-coral" href="{APP}" target="_blank" rel="noopener">Download free</a>
      </div>
    </div>
  </nav>
"""

FOOTER = """  <footer class="footer-bar">
    <div class="container footer-bar-inner">
      <span class="footer-brand">Exercise Snacks: Desk Breaks</span>
      <span class="footer-copy">© 2026 Mithul Mistry</span>
      <nav class="footer-links">
        <a href="/guides/">Guides</a>
        <a href="/entitymap.html">EntityMap</a>
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Use</a>
        <a href="/llm-info">AI Info</a>
      </nav>
    </div>
  </footer>
"""

STYLE = """  <style>
    .em-wrap{max-width:820px;margin:0 auto;padding:3rem 1.5rem 4rem}
    .em-wrap h1{font-size:clamp(2.1rem,4.5vw,3rem);margin-bottom:.6rem}
    .em-head{color:var(--mid);font-size:.95rem;margin-bottom:2.5rem}
    .em-head code{background:var(--grey-light);padding:.1em .4em;border-radius:4px}
    .ent{border-top:1px solid var(--grey-border);padding-top:2rem;margin-top:2.5rem}
    .ent h2{font-size:1.5rem;margin-bottom:.3rem}
    .ent h3{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--mid);margin-top:1.5rem}
    .meta{font-size:.9rem;color:var(--mid);margin-bottom:.6rem}
    .type{background:var(--sage-light);color:#0a6040;border-radius:var(--radius-pill);padding:.15em .7em;font-size:.82rem;font-weight:600}
    .desc{margin-bottom:.5rem}
    .chunks li{margin-bottom:1.1rem}
    .chunks blockquote{border-left:3px solid var(--coral);padding-left:1rem;margin:0 0 .35rem;color:var(--dark)}
    .chunks cite{font-size:.85rem;color:var(--mid);font-style:normal}
    .rels li{margin-bottom:.5rem;font-size:.95rem}
    .rels code{background:var(--coral-light);color:#a8391a;padding:.12em .5em;border-radius:4px;font-size:.85rem}
    .conf{font-size:.78rem;color:var(--mid)}
    .ctx{font-size:.85rem;color:var(--mid)}
    .none{color:var(--mid)}
    .em-wrap a{color:#a8391a;text-decoration:underline}
    .changelog{background:var(--grey-light);border-radius:var(--radius-md);padding:1.1rem 1.3rem;font-size:.9rem;color:var(--mid);margin-bottom:2rem}
  </style>"""


def entity_section(ent):
    chunks = "".join(
        f'<li><blockquote>{e(c["text"])}</blockquote>'
        f'<cite><a href="{e(c["sourceUrl"])}">{e(c["pageTitle"])}</a> · {e(c["publisher"])}'
        + (f' · {e(c["contentType"])}' if c.get("contentType") else "")
        + "</cite></li>"
        for c in ent["hasChunks"]
    )
    rels = "".join(
        f'<li><code>{e(r["predicate"])}</code> → {e(r["targetName"])}'
        + (f' <span class="conf">{e(r["confidence"])}</span>' if r.get("confidence") else "")
        + (f'<br><span class="ctx">{e(r["context"].get("condition", ""))}</span>' if r.get("context") else "")
        + "</li>"
        for r in ent.get("relations", [])
    ) or '<li class="none">none</li>'
    same = f' · <a href="{e(ent["sameAs"])}">sameAs</a>' if ent.get("sameAs") else ""
    return f"""    <section class="ent" id="{e(ent['entityId'])}">
      <h2>{e(ent['name'])}</h2>
      <p class="meta"><code>{e(ent['entityId'])}</code> · <span class="type">{e(ent['@type'])}</span>{same}</p>
      <p class="desc">{e(ent['description'])}</p>
      <h3>Chunks</h3><ul class="chunks">{chunks}</ul>
      <h3>Relations</h3><ul class="rels">{rels}</ul>
    </section>"""


def main():
    d = json.loads((ROOT / "entitymap.json").read_text(encoding="utf-8"))
    sections = "\n".join(entity_section(x) for x in d["entities"])
    changelog = (
        f'    <div class="changelog"><strong>Change log.</strong> {e(d["changeLog"])}</div>\n'
        if d.get("changeLog") else ""
    )
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="EntityMap for Exercise Snacks — the machine-readable entity and relation map for this site, in human-readable form.">
  <link rel="canonical" href="https://exercise-snacks.app/entitymap.html">
  <title>EntityMap — Exercise Snacks</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <link rel="icon" type="image/png" href="/img/favicon.png">
{STYLE}
</head>
<body>
{NAV}
  <main class="em-wrap">
    <h1>EntityMap</h1>
    <p class="em-head">
      EntityMap v{d['version']} · publisher <strong>{e(d['publisher']['name'])}</strong> ·
      generated {e(d['generated'][:10])} · status <code>{e(d['verificationStatus'])}</code><br>
      {len(d['entities'])} entities · {sum(len(x['hasChunks']) for x in d['entities'])} chunks ·
      {sum(len(x.get('relations', [])) for x in d['entities'])} relations ·
      machine-readable: <a href="/entitymap.json">entitymap.json</a>
    </p>
{changelog}{sections}
  </main>
{FOOTER}</body>
</html>
"""
    (ROOT / "entitymap.html").write_text(out, encoding="utf-8")
    print(f"entitymap.html: {len(d['entities'])} entities, {len(out)} bytes")


if __name__ == "__main__":
    main()
