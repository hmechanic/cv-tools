# Repository Guidelines

## Project Structure & Module Organization

The generator logic lives in `scripts/`: `generate_latex.py` loads YAML, resolves BibTeX entries, and renders Jinja templates, while `use_LLM.py` contains optional Groq/OpenRouter integrations. CV data and publication samples belong in `config/`. Layout code is under `template/`, with the main `template.tex.jinja`, reusable section fragments in `template/sections/`, and the LaTeX class in `template/resume.cls`. Generated `.tex` and PDF files go to the ignored `output/` directory. Documentation images are stored in `docs/img/`, and CI workflows are in `.github/workflows/`.

## Build, Test, and Development Commands

- `python -m venv .venv` creates a local environment; activate it before development.
- `pip install --require-hashes -r requirements.lock` installs the reviewed dependency set reproducibly.
- `./run.sh` generates `output/output.tex` and compiles `output/output.pdf` with `pdflatex`.
- `./run.sh --tex-only --no-deps` quickly renders LaTeX without installing dependencies or requiring a LaTeX engine.
- `./run.sh -c config/cv.yaml -o output/custom.tex` exercises explicit input and output paths.
- `docker build -t cv-tools .` builds the TeX Live-based development image used for reproducible generation.

## Coding Style & Naming Conventions

Use four-space indentation and PEP 8-style `snake_case` for Python functions and variables. Keep imports grouped at the top and add short docstrings to public helpers. Shell scripts use Bash, uppercase names for constants such as `OUTPUT_DIR`, and lowercase function names. Preserve LF line endings as required by `.gitattributes`. Name Jinja section files after their YAML section type, for example `template/sections/experience.jinja`. No formatter or linter is currently configured, so keep changes consistent with surrounding code.

## Testing Guidelines

There is no automated unit-test suite. Every change should at least pass `./run.sh --tex-only --no-deps`; template or LaTeX changes should also pass `./run.sh` and produce a readable PDF. Check both English and Spanish configurations when changing language-sensitive behavior. Do not commit generated `output/` artifacts.

## Commit & Pull Request Guidelines

History generally uses short, imperative, scoped prefixes such as `feat:`, `fix:`, `docs:`, and `ci:`. Prefer messages like `fix: escape special characters in headings`. Pull requests should explain the behavior changed, list validation commands, link relevant issues, and include before/after screenshots for visible PDF or template changes.

## Security & Configuration

Keep API keys in the ignored `.env` file; never commit credentials. Treat `config/job_offer.txt`, `config/longProfile.txt`, and personal CV variants as private inputs. LLM-related testing may send resume and job-offer content to an external provider, so use sanitized fixtures when possible.
