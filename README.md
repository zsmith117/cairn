# UX Research SOP Library

A self-contained web app organizing 9 UX research SOPs, 40 checklists, and 49 templates for B2B industrial research operations.

## Open it

Double-click **`UX Research SOP Library.html`**. The app runs entirely offline in your browser — no install, no server.

## Two ways to use it

Toggle between modes at the top of the sidebar:

- **Project Guide** (default) — five research phases from kickoff to close. Each phase shows the work, references the SOPs you'll need, and the completion checklist saves locally so you can pick up where you left off.
- **SOP Library** — the same SOPs, checklists, and templates organized by lifecycle phase for reference browsing.

## Features

- **Procedure** — the full SOP, with a scroll-spy table of contents on the right.
- **Checklists** — collapsible checklists per SOP, with proper task-list checkboxes.
- **Templates** — collapsible form templates per SOP, with editable tables.
- **Phase checkboxes** — task lists inside the Project Guide phases persist in `localStorage`. Sidebar and home cards show your completion %.
- **Cross-references** — each SOP shows "Used in: Phase X" pills linking back to the relevant guide phase.
- **Cmd-K** (or `/`) — search across SOPs, checklists, templates, *and* guide phases.
- **Open in Word** — at the bottom of any checklist/template (and the top of each procedure), download a `.doc` you can save locally and edit in Microsoft Word.
- **Theme toggle** — light/dark, bottom-left of the sidebar.

## Sharing

The HTML file is fully portable. To send it to someone, just attach `UX Research SOP Library.html` to an email or drop it into a shared drive. They double-click and it works.

## Editing the content

The source markdown files live in `source/`. If you want to update an SOP:

1. Edit any file in `source/markdown/`, `source/Checklists/`, or `source/Templates/`.
2. Run the build script to regenerate the HTML:

   ```
   cd source
   python3 build_app.py
   ```

   This rewrites `source/index.html`. Copy that over the top-level `UX Research SOP Library.html` when you're happy.

Python 3.8+ is the only dependency. The first build downloads `marked.min.js` (~30 KB) and caches it as `source/.marked.min.js`.

## File map

```
UX Research SOP Library.html    ← the app
README.md                       ← this file
source/
  build_app.py                  ← bundles markdown → HTML
  markdown/                     ← 9 SOPs
  Checklists/                   ← 40 checklists (after dedupe)
  Templates/                    ← 49 templates (after dedupe)
  phases/                       ← 5 Project Guide phase pages
```
