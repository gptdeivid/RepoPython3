## Purpose
Short, actionable instructions for AI coding agents working on this repository (simple Flask login demo).

## Big picture
- Single-process Flask app in `app.py` (no separate backend/service). Entrypoint runs `app.run(debug=True)` on `0.0.0.0:5000`.
- Templates live in `templates/` (Spanish UI). Static assets in `static/` (only `style.css` present).
- In-memory `USERS` dict in `app.py` is the current user store (no DB).

## Key files to inspect
- `app.py` — routes: `/` (login page), `/login` (POST handler), `/welcome`, `/logout`. Also contains `dated_url_for` (cache-busting helper) and `app.secret_key` (hardcoded).
- `templates/login.html` and `templates/welcome.html` — Jinja2 templates; use `get_flashed_messages()` for toast notifications.
- `static/style.css` — visual styles referenced by templates.
- `requirements.txt` — currently only `Flask==2.3.3`.

## Developer workflows / common commands
- Create venv and install deps:
  - `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`
- Run app locally:
  - `python app.py` (starts debug server on port 5000)
- Useful quick checks:
  - Valid logins: `admin@test.com` / `admin123`, `user@test.com` / `user123`, `demo@demo.com` / `demo`.

## Project-specific conventions & important patterns
- Templates currently reference CSS using absolute Windows paths (e.g. `C:\Users\...\static\style.css`). When modifying templates, replace those with Jinja2 static URL helper:
  - `{{ url_for('static', filename='style.css') }}`
  - This keeps `dated_url_for` cache-busting behavior working.
- `dated_url_for(endpoint, **values)` appends `?q=<mtime>` for static files. Preserve it when changing static asset handling.
- Session and flash usage:
  - `session['username']` and `session['email']` are used to gate `/welcome`.
  - Use `flash()` for user-visible messages; templates already render flashes into a JS toast.
- Secrets: `app.secret_key` is hardcoded. Do NOT commit production secrets — prefer `os.environ.get('FLASK_SECRET')` if adding real deployments.

## Integration & external deps
- External assets loaded from CDNs in templates: Font Awesome and Google Fonts. No database, external APIs, or background jobs in the repo.

## When making changes, watch for these pitfalls
- Don't break the in-memory `USERS` structure if you only intend to change UI; tests and demo accounts rely on those keys.
- Fix templates to use `url_for('static', ...)` instead of absolute filesystem paths — failing to do so breaks static serving on other machines.
- Keep `dated_url_for` behavior if you add or rename static files; it prevents stale CSS in browsers.
- If you add persistent storage, update README and remove hardcoded credentials and secret key.

## Example actionable edits an agent may be asked to do
- Replace hardcoded CSS paths in both templates with `{{ url_for('static', filename='style.css') }}`.
- Move `app.secret_key` to read from environment and add a short comment explaining why.
- Add a README section with run instructions and demo credentials (see 'Developer workflows' above).

## Where to leave notes / PR description hints
- Explain any change that affects runtime behavior (sessions, static files, or routes). Mention demo credentials if you update them.
- Small UI fixes: show the changed template line and note that `dated_url_for` was preserved.

If anything here is unclear or you'd like me to expand examples (e.g., a ready PR that fixes the template paths and secret handling), tell me which one to implement next.
