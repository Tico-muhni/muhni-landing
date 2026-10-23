# Site build tools

The public pages share one header, footer and stylesheet. To keep them identical they are generated.

- `tools/chrome.py` has the shared header (menu, services mega menu, mobile sheet), footer and floating quick actions.
- `tools/build_pages.py` regenerates the public pages from their existing content: `python3 tools/build_pages.py` (or pass page names: `home br refinance upgraders investors blog_index articles docs thankyou lecture lottery`).
- `assets/css/tico.css`, `assets/js/*.js` and `assets/img/*` are served as static files.

Hidden / noindex pages (`/check`, `/street`, `/card`, `/clients`, `/topsecret`, `/tf-*`, `/lecture/join`, `/mashov`, `/mismachim`, `/itrot`, `/ashrai`) are not generated and keep their own design.

The builder reads the original page from `origin/main` (`git show`), so run it on a branch cut from `main`. After the redesign is merged, edit the generated HTML directly or update the builder, not both.

Videos: set `window.TICO_VIDEO_ID = '<youtube id>'` before `tico.js` loads (one per language) to replace the "coming soon" message in the intro video dialog.
