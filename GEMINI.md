---
alwaysApply: true
always_on: true
trigger: always_on
description: PHYD57 Course Website Guidelines
---

# PHYD57H3 Course Repository Guidelines

### Scope & Structure
* This repository (`phyd57h3`) is dedicated exclusively to **PHYD57H3: Advanced Computational Methods in Physics**.
* **Directory Layout**:
  - `notes/`: Official lecture notes and syllabus.
  - `problems/`: Problem sets, past exam prompts, and problem solutions.
  - `simulations/`: Numerical simulation code (C, Fortran, CUDA, OpenMP, Python).
  - `reference/`: Technical references, compiler guides, Linux HPC tutorials, and cluster connection workflows (`art-1`, `art-16`).
* **DO NOT put general blog posts here**. General articles belong in the main blog (`/home/igorkan/repos/quarto-writing`).

### Repository Architecture (Public Deployment Site)
* This is the **Public** deployment repository.
* `origin`: `https://github.com/igor-kan/phyd57h3.git` (Triggers public GitHub Pages deployment)
* Contains ONLY published materials and sanitized guides.
* All raw drafts (`draft: true`), unredacted passwords, and solutions belong strictly in the private companion repository at `/home/igorkan/repos/phyd57h3-drafts/`.

### Drafts, Security & Credentials
* "Publish" = ensure `draft: true` is not present (or set to `draft: false`).
* "Unpublish" / "Draft" = set `draft: true` in the frontmatter.
* When `draft: true` is set, Quarto automatically excludes the document from public website rendering.
* **Sensitive Credentials (e.g. cluster passwords)**:
  - NEVER publish raw passwords to the public website.
  - Public documents must redact credentials: `[REDACTED — Provided in class / stored in private draft]`.
  - Full credentials may only be stored in documents marked `draft: true`, ensuring they reside solely in the private backup repository.

### UI & Styling Standards
* Adhere strictly to the Notion.so minimalist aesthetic in light and dark mode.
* Footer must display: `© 2026 Igor Kan`.
