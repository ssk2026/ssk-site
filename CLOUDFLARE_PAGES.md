# Cloudflare Pages deployment

The site can be exported from Django into plain HTML, CSS, JavaScript, images,
and PDFs. Cloudflare Pages serves the generated `dist` directory, so the local
development computer does not need to stay online.

## Local verification

```powershell
.\venv\Scripts\python.exe build_static.py
.\venv\Scripts\python.exe -m http.server 8080 --directory dist
```

Open `http://127.0.0.1:8080`. Stop the preview server with `Ctrl+C`.

## Cloudflare Pages settings

Connect the GitHub repository in **Workers & Pages > Create > Pages > Connect
to Git** and use these build settings:

```text
Production branch: main
Framework preset: None
Build command: python -m pip install -r requirements-deploy.txt && python build_static.py
Build output directory: dist
Root directory: /
```

Every push to `main` then triggers a new production deployment. Pull request
branches receive preview deployments.

## New Cloudflare Worker setup screen

Cloudflare may show the newer Worker setup screen instead of the Pages form.
This repository includes `wrangler.jsonc`, so that screen can also deploy the
same static site. Use:

```text
Project name: ssk-site
Build command: python -m pip install -r requirements-deploy.txt && python build_static.py
Deploy command: npx wrangler deploy
Preview command: npx wrangler preview
```

The Worker serves the generated `dist` directory as static assets. Git pushes
still trigger automatic builds and deployments.

## Updating content

Editors can sign in at `https://app.pagescms.org`, select the
`ssk2026/ssk-site` repository, and edit content in the browser. Saving an item
commits it to GitHub and triggers a Cloudflare Pages deployment automatically.

See `CONTENT_MANAGEMENT.md` for the editor setup and handover workflow.

## Custom domain

After buying a domain, add it under the Pages project's **Custom domains**.
Cloudflare will show the nameservers or DNS records that must be configured at
the registrar. HTTPS is issued after DNS verification succeeds.
