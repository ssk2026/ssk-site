# Content management

Public content is stored as one JSON file per entry. Pages CMS edits these
files through a browser and commits each change to GitHub. Cloudflare Pages
then rebuilds the public site automatically.

## Directories

- `events/`: major events
- `briefings/`: conference presentations
- `notices/`: notices
- `papers/`: academic papers and books

The filename becomes the public URL slug. Existing numeric filenames preserve
the current URLs. New files receive a timestamp filename automatically.

Set `published` to `false` to keep an entry as a draft. Optional empty fields
are handled by the site, and uploaded assets are stored under `media/events/`.

For local validation and preview:

```powershell
python manage.py check_content
python manage.py runserver
```

See `CONTENT_MANAGEMENT.md` for the browser-based editing workflow.
