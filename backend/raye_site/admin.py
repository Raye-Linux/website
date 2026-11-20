"""raye-site-admin: look at the list on launch day.

    raye-site-admin count            how many pending, confirmed, unsubscribed
    raye-site-admin list             confirmed addresses, one per line
    raye-site-admin export           confirmed addresses as CSV on stdout
    raye-site-admin delete ADDRESS   erase an address (deletion request)
    raye-site-admin purge            run the cleanup now (applications too)

    raye-site-admin applications count | list [--status S] | show REF
    raye-site-admin applications notify [--all]   tell the staff channel again
    raye-site-admin applications delete REF       erase one (deletion request)
    raye-site-admin applications forget --email A | --discord NAME

There is deliberately no command that sends mail to the list.
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone

from . import applications as apps
from .config import Config
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
    a = sub.add_parser("applications", help="applications to join the team")
    asub = a.add_subparsers(dest="what", required=True)
    asub.add_parser("count")
    al = asub.add_parser("list")
    al.add_argument("--status", choices=apps.STATUSES)
    ash = asub.add_parser("show")
    ash.add_argument("ref")
    an = asub.add_parser("notify")
    an.add_argument("--all", action="store_true", help="also the ones past their retries")
    ad = asub.add_parser("delete")
    ad.add_argument("ref")
    af = asub.add_parser("forget")
    af.add_argument("--email")
    af.add_argument("--discord")
    args = parser.parse_args(argv)

    store = Store(args.db)
    store.init()
    join = apps.Store(args.db)
    join.init()

    if args.command == "applications":
        return applications_command(args, join)

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
        print(join.purge())
    elif args.command == "launch-mail":
        n = store.queue_announcement("launch", dry_run=not args.send)
        print(f"{'queued' if args.send else 'would queue'}: {n}")
    return 0


def applications_command(args, join) -> int:
    if args.what == "count":
        for key, value in join.counts().items():
            print(f"{key}: {value}")
    elif args.what == "list":
        for row in join.list(status=args.status):
            print(f"{row['id']}\t{row['status']}\t{row['role']}\t{row['discord']}\t"
                  f"{_when(row['created_at'])}")
    elif args.what == "show":
        row = join.get(args.ref)
        if row is None:
            print("not found", file=sys.stderr)
            return 1
        for key, value in row.items():
            if key.endswith("_at") and value:
                value = _when(value)
            print(f"{key}: {value}")
    elif args.what == "notify":
        # the webhook path comes from the same place as the service's
        config = Config.from_env()
        sent, failed = apps.Applications(join, config.join_webhook_paths,
                                         background=False).deliver_pending(every=args.all)
        print(f"sent: {sent}, failed: {failed}")
        return 1 if failed else 0
    elif args.what == "delete":
        if not join.delete(args.ref):
            print("not found", file=sys.stderr)
            return 1
        print("deleted")
    elif args.what == "forget":
        print(f"deleted: {join.delete_person(email=args.email, discord=args.discord)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
