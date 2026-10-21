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

## Updating content

1. Edit `content/events.json` or `content/notices.json`.
2. Add images or PDFs under `media/` and use `/media/...` paths in JSON.
3. Run `python manage.py check_content` and `python build_static.py`.
4. Commit and push the changes to GitHub.

## Custom domain

After buying a domain, add it under the Pages project's **Custom domains**.
Cloudflare will show the nameservers or DNS records that must be configured at
the registrar. HTTPS is issued after DNS verification succeeds.
