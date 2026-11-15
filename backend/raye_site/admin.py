"""raye-site-admin: look at the list on launch day.

    raye-site-admin count            how many pending, confirmed, unsubscribed
    raye-site-admin list             confirmed addresses, one per line
    raye-site-admin export           confirmed addresses as CSV on stdout
    raye-site-admin delete ADDRESS   erase an address (deletion request)
    raye-site-admin purge            run the cleanup now

There is deliberately no command that sends mail to the list.
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone

from .store import Store

DEFAULT_DB = os.path.join(os.environ.get("STATE_DIRECTORY", "/var/lib/raye-site").split(":")[0],
                          "site.db")


def _when(ts) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _cell(value: str) -> str:
    # a spreadsheet would run a cell starting with one of these as a formula
    return "'" + value if value[:1] in ("=", "+", "-", "@", "\t", "\r") else value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="raye-site-admin",
                                     description="Launch list of rayelinux.com")
    parser.add_argument("--db", default=DEFAULT_DB, help="database file")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("count", help="pending, confirmed and unsubscribed addresses")
    sub.add_parser("list", help="confirmed addresses")
    sub.add_parser("export", help="confirmed addresses as CSV")
    d = sub.add_parser("delete", help="erase one address")
    d.add_argument("address")
    sub.add_parser("purge", help="remove expired entries now")
    lm = sub.add_parser("launch-mail", help="queue the one launch email (dry run unless --send)")
    lm.add_argument("--send", action="store_true", help="really queue it")
    args = parser.parse_args(argv)

    store = Store(args.db)
    store.init()

    if args.command == "count":
        for key, value in store.counts().items():
            print(f"{key}: {value}")
        print(f"queued mails: {store.queue_size()}")
    elif args.command == "list":
        for row in store.confirmed():
            news = "news" if row["news"] else "-"
            print(f"{row['email']}\t{row['lang']}\t{news}\t{_when(row['confirmed_at'])}")
    elif args.command == "export":
        out = csv.writer(sys.stdout)
        out.writerow(["email", "lang", "news", "confirmed_at"])
        for row in store.confirmed():
            out.writerow([_cell(row["email"]), row["lang"], "yes" if row["news"] else "no",
                          _when(row["confirmed_at"])])
    elif args.command == "delete":
        if not store.delete(args.address):
            print("not found", file=sys.stderr)
            return 1
        print("deleted")
    elif args.command == "purge":
        print(store.purge())
    elif args.command == "launch-mail":
        n = store.queue_announcement("launch", dry_run=not args.send)
        print(f"{'queued' if args.send else 'would queue'}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
