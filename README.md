# rayelinux.com

The website of Raye Linux, French first, English too: static pages, a
small Python backend for the mailing list (double opt-in), bug reports and
the help bubble, and the files to deploy it.

- `site/` the pages, built by `tools/build_pages.py` (committed)
- `backend/` the server (Python, standard library only)
- `deploy/` nginx, systemd and firewall files, and `deploy.sh`
- `tools/` page and text builders

## The V1 site (not online yet)

`site-v1/` is written by the same build (`tools/site_v1.py`, text in
`tools/site_v1_text.py`, `tools/site_v1_join_text.py` and
`tools/legal_v1_text.py`). It adds the "Join the team" pages, the Community
page and the V1 legal pages (marked as a draft). Two backend endpoints serve it:

- `POST /api/join`: an application (JSON or a plain form). Kept in the
  backend's SQLite file (`applications` table, no IP address), then posted
  to a private staff channel through a Discord webhook. The webhook address
  is read from `/etc/raye-site/join-webhook` (one line, a
  `https://discord.com/api/webhooks/<id>/<token>` address, root only, 0600);
  systemd hands it over as the credential `smtp_join-webhook`. Without it,
  applications are still kept and sent once it exists
  (`raye-site-admin applications notify`).
- `GET /api/community`: the Discord server name, member and online counts,
  asked from Discord's public invite address by the server, kept 10 minutes.

`raye-site-admin applications count|list|show|notify|delete|forget` reads
and manages the applications until the staff panel exists.

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
