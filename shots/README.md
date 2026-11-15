# Screenshots of the V1 site

The only place the V1 site takes its screenshots from. `tools/site_v1.py`
copies the picture files of this folder into `<site>/assets/shots/` at every
build and removes whatever else is there (the coming-soon page's 0.2
pictures share some names: `lock`, `settings`, `store`).

Each screenshot is three files, for each language:

    <id>-<lang>-1600.webp   <id>-<lang>-800.webp   <id>-<lang>-1600.jpg

`<id>` is a key of `SHOTS` in `tools/site_v1_text.py`, which also says what
the picture has to show. Until the three files exist, the page shows a
labelled placeholder.

`manifest.json` says which Raye version and which day each screenshot
shows, one entry per `<id>-<lang>`:

    {"desktop-fr": {"version": "1.0", "date": "2026-12-01"}}

At launch, `test_site_v1.py` refuses a screenshot whose entry is missing or
is not of the version the site speaks for.
