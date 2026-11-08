set -e -o pipefail
cd /home/claude/daraj_web
python3 covers.py >/dev/null
python3 build.py | tail -1
rm -f site/daraj-article-*.html
rm -rf final
python3 seo.py | tail -1
python3 rebrand.py
