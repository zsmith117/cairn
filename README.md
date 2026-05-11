# Throughline

A working project workspace and reference library for UX research operations.
Built for B2B industrial research where evidence has to survive procurement,
engineering, and the C-suite.

Live demo: **https://zsmith117.github.io/throughline/**

## Open it

Visit the URL above, or double-click `Throughline.html` to run it locally
in your browser. No install, no server, no account — everything saves in
`localStorage` and stays on your device.

## Two ways to use it

Toggle between modes at the top of the sidebar:

- **Project Guide** (default) — a 5-phase runbook for an entire research
  project, from kickoff through delivery. Each phase shows your in-progress
  artifacts, recommends the right starter for that phase, and tracks your
  completion as you go.
- **SOPs** — the underlying reference library: 9 UX research SOPs, 40
  checklists, 49 templates, organized for browsing.

## Features

### Project workspace
- **Create multiple projects** with name, owner, stakeholder, description.
- **Phase progression** — Project Initiation → Research Design → Field Work
  → Analysis → Delivery & Close. Phase advances automatically when its
  completion checklist hits 100%.
- **Next-action card** on every project home points at the right artifact
  to work on next.
- **Autosave** — everything you type persists immediately. A subtle "Saved"
  toast confirms each write.

### Fillable artifacts
- **25 of 49 templates have bespoke forms** that render as interactive UI:
  Research Brief, Plan, Interview Guide, Screener, Session Notes,
  Theme Development, Insight Development, Executive Summary, and more.
- **The remaining 24 templates** are editable in place — `___` blanks
  become text inputs, table cells become `contenteditable`, checklist
  `- [ ]` items become live checkboxes.
- **Multi-instance support** — Session Notes, Field Notes, Workshop
  Agendas, Health Checks, etc. can have N instances per project (one
  per session, visit, workshop, audit, …) with per-instance status.
- **Section completeness** — each form section shows `3/5` filled in
  mono next to the title, with a green ✓ when complete.

### Working with the docs
- **Open in Word** — every artifact exports to a `.doc` populated with
  your project name and filled-in data. Filename prefixed with the
  project so files stay organized.
- **Compile Readout** — one click on the project home bundles every
  filled artifact into a single Word document with a cover page,
  phase grouping, and properly nested headings. Ready to send.
- **Export project as JSON** — backup or move a project between devices.

### Discovery and recovery
- **⌘K / `/`** search across SOPs, checklists, templates, and phases.
  When a project is active, your in-progress artifacts surface above
  reference results.
- **Undo for delete** — accidentally delete an instance or a whole
  project? An undo toast appears for 8 seconds. One click restores it.
- **Welcome banner** explains the workflow on your first project visit.

### Accessibility & responsive
- WCAG AA contrast on all status indicators.
- Inline text inputs carry derived `aria-label`s from preceding context.
- Hidden `aria-live` announcer reads each autosave + milestone.
- Mobile drawer navigation below 880px viewport.

## Editing the content

The source markdown files live in `source/`. To update an SOP:

1. Edit any file in `source/markdown/`, `source/Checklists/`,
   `source/Templates/`, or `source/phases/`.
2. Run the build script:

   ```
   cd source
   python3 build_app.py
   ```

3. Copy the regenerated `source/index.html` over the top-level
   `Throughline.html`.

Python 3.8+ is the only dependency. The first build downloads
`marked.min.js` (~30 KB) and caches it.

## File map

```
Throughline.html        ← the app (drop into any browser, no server)
README.md
source/
  build_app.py         ← bundles markdown + form schemas → HTML
  markdown/            ← 9 SOPs
  Checklists/          ← 46 source files → 40 after dedupe
  Templates/           ← 52 source files → 49 after dedupe
  phases/              ← 5 Project Guide phase pages
```
