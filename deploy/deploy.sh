#!/bin/sh
# Deploy rayelinux.com to its server. Idempotent: run it again after any
# change. Needs ssh to debian@<host> with passwordless sudo.
#
# The addresses of the server and of what it talks to are not in the repo:
# copy deploy/site.env.example to deploy/site.env (ignored by git) and fill
# it in. The @NAME@ marks in deploy/ are replaced from it before the copy.
#
#   deploy/deploy.sh                 # tests, then deploy to $TARGET
#   RAYE_SITE_TARGET=debian@host deploy/deploy.sh
#   SKIP_TESTS=1 deploy/deploy.sh
set -eu

HERE=$(cd "$(dirname "$0")/.." && pwd)
STAGE=raye-site-stage

cd "$HERE"

if [ ! -r deploy/site.env ]; then
    echo "deploy/site.env is missing: copy deploy/site.env.example and fill it in" >&2
    exit 1
fi
. ./deploy/site.env
TARGET=${RAYE_SITE_TARGET:-$TARGET}
# where build_support_kb.py finds the release notes and the Discord texts
export RAYE_PUBLISH RAYE_DISCORD_TEXTS

if [ "${SKIP_TESTS:-0}" != 1 ]; then
    echo "== tests"
    (cd backend && python3 -m unittest discover -s tests -t tests -q)
fi

echo "== help bubble knowledge base"
# old answers must not ship: a changed page, handbook or release note
# that is not in the file stops here
python3 -B tools/build_support_kb.py --check

echo "== copy to $TARGET:~/$STAGE"
ssh "$TARGET" "mkdir -p ~/$STAGE"
# pages that are built but not public yet stay off the server
EXCLUDES=$(mktemp)
RENDERED=$(mktemp -d)
trap 'rm -rf "$EXCLUDES" "$RENDERED"' EXIT
sed -n 's|^/|/site/|p' deploy/not-yet-public > "$EXCLUDES"
# the deploy files with their @NAME@ marks filled in from site.env
cp -a deploy "$RENDERED/deploy"
rm -f "$RENDERED/deploy/site.env" "$RENDERED/deploy/site.env.example"
find "$RENDERED/deploy" -type f -exec sed -i \
    -e "s|@PROXY_IP@|$PROXY_IP|g" -e "s|@MAIL_IP@|$MAIL_IP|g" \
    -e "s|@MAIL_TLS_NAME@|$MAIL_TLS_NAME|g" -e "s|@LLM_IP@|$LLM_IP|g" \
    -e "s|@BUGS_API_IP@|${BUGS_API_IP:-}|g" {} +
if grep -rq '@[A-Z_]*_\(IP\|NAME\)@' "$RENDERED/deploy"; then
    echo "deploy/site.env leaves a @NAME@ mark unfilled" >&2
    exit 1
fi
rsync -rlt --safe-links --delete --delete-excluded --chmod=D755,F644 \
    --exclude '__pycache__' --exclude '*.pyc' --exclude 'tests/' \
    --exclude-from="$EXCLUDES" \
    site backend "$RENDERED/deploy" README.md "$TARGET:$STAGE/"

echo "== install"
ssh "$TARGET" "sudo sh -s" <<'REMOTE'
set -eu
STAGE=/home/debian/raye-site-stage
export DEBIAN_FRONTEND=noninteractive

if ! dpkg -s nginx >/dev/null 2>&1; then
    apt-get update -q
    apt-get install -y -q --no-install-recommends nginx
fi

# files: root-owned, read-only for everyone else
install -d -m 0755 -o root -g root /var/www/raye-site /opt/raye-site /opt/raye-site/backend
rsync -rlt --safe-links --delete --chown=root:root --chmod=D755,F644 "$STAGE/site/" /var/www/raye-site/
rsync -rlt --safe-links --delete --chown=root:root --chmod=D755,F644 "$STAGE/backend/" /opt/raye-site/backend/
chmod 755 /opt/raye-site/backend/raye-site-server /opt/raye-site/backend/raye-site-admin
install -m 0644 -o root -g root "$STAGE/README.md" /opt/raye-site/README.md
python3 -m compileall -q /opt/raye-site/backend/raye_site

# SMTP settings live here (root only); the service reads them as a credential
install -d -m 0700 -o root -g root /etc/raye-site

install -m 0755 -o root -g root "$STAGE/deploy/raye-site-admin" /usr/local/sbin/raye-site-admin

# systemd
for unit in raye-site.service raye-site-smtp.path raye-site-smtp.service; do
    install -m 0644 -o root -g root "$STAGE/deploy/systemd/$unit" "/etc/systemd/system/$unit"
done
systemd-analyze verify /etc/systemd/system/raye-site.service
systemctl daemon-reload
systemctl enable -q raye-site.service raye-site-smtp.path
systemctl restart raye-site.service
systemctl start raye-site-smtp.path

# nginx
for snippet in raye-site-headers.conf raye-site-limitkey.conf; do
    install -m 0644 -o root -g root "$STAGE/deploy/nginx/$snippet" "/etc/nginx/snippets/$snippet"
done
install -m 0644 -o root -g root "$STAGE/deploy/nginx/raye-site.conf" \
    /etc/nginx/sites-available/raye-site
ln -sfn /etc/nginx/sites-available/raye-site /etc/nginx/sites-enabled/raye-site
rm -f /etc/nginx/sites-enabled/default
nginx -t -q
systemctl enable -q nginx
systemctl reload-or-restart nginx

# firewall: port 80 from the reverse proxy only
install -m 0644 -o root -g root "$STAGE/deploy/nftables/raye-site.nft" /etc/nftables.d/raye-site.nft
nft -c -f /etc/nftables.conf
systemctl reload-or-restart nftables

# checks
for i in 1 2 3 4 5 6 7 8 9 10; do
    curl -fsS http://127.0.0.1:8081/api/health >/dev/null 2>&1 && break
    sleep 1
done
curl -fsS http://127.0.0.1:8081/api/health
curl -fsS -o /dev/null -w 'site %{http_code}\n' -H 'Host: rayelinux.com' http://127.0.0.1/
systemctl is-active raye-site.service raye-site-smtp.path nginx nftables
REMOTE
echo "== done"
