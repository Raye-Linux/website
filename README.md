# rayelinux.com

The website of Raye Linux, French first, English too: static pages, a
small Python backend for the mailing list (double opt-in), bug reports and
the help bubble, and the files to deploy it.

- `site/` the pages, built by `tools/build_pages.py` (committed)
- `backend/` the server (Python, standard library only)
- `deploy/` nginx, systemd and firewall files, and `deploy.sh`
- `tools/` page and text builders

## Build the pages

    python3 tools/build_pages.py

## Test

    cd backend && python3 -m unittest discover -s tests -t tests

## Deploy

Copy `deploy/site.env.example` to `deploy/site.env` (not in git), fill in
the addresses, then run `deploy/deploy.sh`. It runs the tests first.

## License

GPL-3.0-or-later (`LICENSE`).

## Links

- Website: https://rayelinux.com
- Discord: https://discord.gg/TrxhUkabyB (questions, bug reports, news)
