# Stage 2: SEO site — clean URLs, static English + Arabic pages (ar/), hreflang, schema, sitemap, articles everywhere
import os, re, json, shutil, html as H
from bs4 import BeautifulSoup
SRC = "/home/claude/daraj_web/site"
OUT = "/home/claude/daraj_web/final"
DOMAIN = "https://daraj.pages.dev"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/ar")

exec(open("/home/claude/daraj_web/articles_data.py", encoding="utf-8").read())
RENAME = {"daraj-insights.html": "articles.html"}
ART = [(x["slug"], x["cat"][0], x["cat"][1], x["title"][0], x["title"][1], x["desc"][0], x["desc"][1], x["img"], x["alt"][0], x["alt"][1]) for x in ARTICLES]
BY = {x["img"]: i for i, x in enumerate(ARTICLES)}
PICK = {"daraj-capital.html": ["capital", "invest", "pricing"], "daraj-investors-club.html": ["invest", "capital", "sell"], "daraj-safqa.html": ["sell", "pricing", "cash"],
        "daraj-bedaya.html": ["bedaya", "cash", "pricing"], "daraj-consulting.html": ["ai", "pricing", "cash"], "daraj-departments.html": ["depts", "ai", "cash"],
        "daraj-invest.html": ["invest", "capital", "bedaya"], "daraj-business.html": ["friends", "depts", "ai"], "daraj-private-advisory.html": ["friends", "invest", "capital"]}
PICK = {k: [BY[n] for n in v] for k, v in PICK.items()}
IM = '<div class="im"><svg width="90" height="60" viewBox="0 0 90 60" aria-hidden="true"><rect x="0" y="40" width="20" height="20" rx="3" fill="#E3A93B" opacity="0.5"></rect><rect x="26" y="26" width="20" height="34" rx="3" fill="#E3A93B" opacity="0.75"></rect><rect x="52" y="10" width="20" height="50" rx="3" fill="#E3A93B"></rect></svg></div>'

def get_ar(h):
    m = re.search(r'const AR = (\{.*?\});\s*\nconst EN', h, re.S)
    return json.loads(m.group(1))

def T(ar, k, en, a, tag="span", attrs=""):
    ar[k] = a
    return f'<{tag}{" " + attrs if attrs else ""} data-i18n="{k}">{en}</{tag}>'

NEW_SCRIPT = """<script>
// Every new page opens at the top (unless the link points to a section)
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
function dTop() {
  if (location.hash) { const el = document.getElementById(location.hash.slice(1)); if (el) { el.scrollIntoView({behavior: "instant", block: "start"}); return; } }
  window.scrollTo({top: 0, left: 0, behavior: "instant"});
}
dTop(); window.addEventListener("load", dTop); window.addEventListener("pageshow", dTop);
document.querySelectorAll('a[href]').forEach(a => a.addEventListener("click", () => {
  const u = new URL(a.href, location.href);
  if (u.pathname !== location.pathname && !u.hash) { try { window.parent && window.parent !== window && window.parent.scrollTo(0, 0); } catch (e) {} }
}));
document.querySelectorAll("select").forEach(s => { if (s.options.length) s.options[0].value = ""; });
// Forms. W3F_KEY: Web3Forms access key (requests go to Daraj's private inbox; the key does not reveal the email).
// Until the key is added, a submitted form opens WhatsApp with the request filled in. CAL_URL: Calendly booking link.
const WA = "201002701704", W3F_KEY = "", CAL_URL = "";
const bf = document.getElementById("bookForm");
if (bf) bf.addEventListener("submit", e => {
  e.preventDefault();
  const ar = document.documentElement.dir === "rtl", data = {}, lines = [];
  bf.querySelectorAll("label").forEach(l => {
    const f = l.querySelector("input,select,textarea"); if (!f || f.type === "checkbox") return;
    const lab = ((l.querySelector("span") || {}).textContent || f.name).trim();
    const v = f.tagName === "SELECT" ? f.options[f.selectedIndex].text : f.value.trim();
    if (v) { data[lab] = v; lines.push(lab + ": " + v); }
  });
  if (W3F_KEY) {
    fetch("https://api.web3forms.com/submit", {method: "POST", headers: {"Content-Type": "application/json", Accept: "application/json"},
      body: JSON.stringify(Object.assign({access_key: W3F_KEY, subject: "New Daraj request: " + document.title, from_name: "Daraj website", page: location.href}, data))}).catch(() => {});
  } else {
    const NL = String.fromCharCode(10);
    window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent((ar ? "طلب جديد من موقع درج" : "New request from the Daraj website") + NL + document.title + NL + NL + lines.join(NL)), "_blank");
  }
  bf.hidden = true; const th = document.getElementById("thanks"); th.hidden = false;
  if (CAL_URL) { const a = document.createElement("a"); a.className = "btn btn-gold"; a.href = CAL_URL; a.target = "_blank"; a.rel = "noopener";
    a.textContent = ar ? "اختر موعد مكالمتك الآن ←" : "Pick a time for your call now →"; a.style.marginTop = "18px"; th.appendChild(a); }
});
</script>"""

pages = {}
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".html"): continue
    h = open(os.path.join(SRC, f), encoding="utf-8").read()
    for a, b in RENAME.items(): h = h.replace(a, b)
    pages[RENAME.get(f, f)] = h

SITEMAP = []
for fname, h in pages.items():
    ar = get_ar(h)
    # --- nav: Articles visible on every screen, plus an Articles column in the Services menu
    h = re.sub(r'<a href="articles.html" class="hide-m" data-i18n="nav_ins">[^<]*</a>', '<a href="articles.html" data-i18n="nav_ins">Articles</a>', h)
    ar["nav_ins"] = "المقالات"
    col = "<div>" + T(ar, "div_art", '<a href="articles.html" style="color:inherit">Daraj Insights · articles</a>', '<a href="articles.html" style="color:inherit">رؤى درج · المقالات</a>', "h4") + "".join(
        T(ar, f"mn_a{i}", a[3], a[4], "a", f'href="{a[0]}"') + "<br>" for i, a in enumerate(ART)) + T(ar, "mn_all", "All articles →", "كل المقالات ←", "a", 'href="articles.html" style="font-weight:700"') + "</div>"
    h = re.sub(r'(<div class="dd-menu">.*?)(</div>\s*</div>\s*</div>)', lambda m: m.group(1) + "</div>\n          " + col + "\n        </div></div>" if False else m.group(0), h, count=1, flags=re.S)
    # --- "From our articles" on every service and door page
    if fname in PICK:
        cards = "".join(f'<a class="icard" href="{ART[n][0]}"><img src="images/{ART[n][7]}.jpg" alt="{ART[n][8]}" data-alt-ar="{ART[n][9]}" loading="lazy" width="1600" height="900" style="display:block;width:100%;height:170px;object-fit:cover"><div class="bd">{T(ar, f"fa_c{x}", ART[n][1], ART[n][2], "span", "class=\"cat\"")}{T(ar, f"fa_t{x}", ART[n][3], ART[n][4], "h3")}{T(ar, f"fa_d{x}", ART[n][5], ART[n][6], "p")}</div></a>' for x, n in enumerate(PICK[fname]))
        sec = f'''<section class="ivory" id="articles"><div class="wrap">
 <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:40px"><div class="sec-head" style="margin:0">{T(ar,"fa_eb","Daraj Insights","رؤى درج","div",'class="eyebrow"')}{T(ar,"fa_h2","From our articles","من مقالاتنا","h2")}</div>{T(ar,"fa_all","All articles →","كل المقالات ←","a",'class="btn btn-navy" href="articles.html"')}</div>
 <div class="ins">{cards}</div>
</div></section>
'''
        h = h.replace("<footer>", sec + "<footer>", 1)
    # --- footer: articles + services links (internal linking)
    fl = '<nav aria-label="Footer" style="display:flex;flex-wrap:wrap;gap:12px 26px;margin:22px 0 6px">' + "".join(T(ar, f"ft{i}", e, a, "a", f'href="{u}" style="color:#C9D2DE"') for i, (e, a, u) in enumerate([
        ("Daraj Invest", "درج للاستثمار", "daraj-invest.html"), ("Daraj Business", "درج للأعمال", "daraj-business.html"), ("Capital", "كابيتال", "daraj-capital.html"), ("Investors Club", "نادي المستثمرين", "daraj-investors-club.html"),
        ("Safqa", "صفقة", "daraj-safqa.html"), ("Bedaya", "بداية", "daraj-bedaya.html"), ("Consulting", "الاستشارات", "daraj-consulting.html"), ("Departments", "الإدارات", "daraj-departments.html"), ("Private Advisory", "الاستشارات الخاصة", "daraj-private-advisory.html"), ("Articles", "المقالات", "articles.html")])) + "</nav>"
    h = re.sub(r'(<footer><div class="wrap">\s*<div class="fgrid2">.*?</div></div>)', lambda m: m.group(1) + fl, h, count=1, flags=re.S)
    # --- strip the client-side language switcher; each language gets its own crawlable page
    h = re.sub(r'<script>\nconst AR = .*?</script>', NEW_SCRIPT, h, count=1, flags=re.S)
    h = h.replace('<button class="lang" id="langBtn" type="button">العربية</button>', f'<a class="lang" id="langBtn" href="ar/{fname}" hreflang="ar" lang="ar" style="text-decoration:none">العربية</a>')
    # --- SEO head
    title_en = re.search(r"<title>(.*?)</title>", h).group(1)
    desc_en = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    url_en, url_ar = f"{DOMAIN}/{'' if fname == 'index.html' else fname}", f"{DOMAIN}/ar/{'' if fname == 'index.html' else fname}"
    m_img = re.search(r'<figure class="cover"><img src="images/([^"]+)"', h)
    ogimg = m_img.group(1) if m_img else "cash.jpg"
    def headtags(url, title, desc, lang, ld):
        return (f'<link rel="canonical" href="{url}">\n<link rel="alternate" hreflang="en" href="{url_en}">\n<link rel="alternate" hreflang="ar" href="{url_ar}">\n<link rel="alternate" hreflang="x-default" href="{url_en}">\n'
                f'<meta property="og:type" content="{"article" if fname.startswith("article-") else "website"}">\n<meta property="og:site_name" content="Daraj">\n<meta property="og:title" content="{H.escape(title)}">\n<meta property="og:description" content="{H.escape(desc)}">\n<meta property="og:url" content="{url}">\n<meta property="og:locale" content="{"ar_AR" if lang == "ar" else "en_US"}">\n<meta name="twitter:card" content="summary_large_image">\n<meta property="og:image" content="{DOMAIN}/images/{ogimg}">\n'
                f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    def ld_for(lang, title, desc, url):
        org = {"@type": "Organization", "name": "Daraj", "alternateName": "درج", "url": DOMAIN}
        if fname.startswith("article-"):
            return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "inLanguage": lang, "author": org, "publisher": org, "mainEntityOfPage": url}
        if fname == "index.html":
            return {"@context": "https://schema.org", **org, "description": desc, "inLanguage": lang}
        if fname == "articles.html":
            return {"@context": "https://schema.org", "@type": "Blog", "name": title, "description": desc, "inLanguage": lang, "publisher": org, "url": url}
        return {"@context": "https://schema.org", "@type": "Service", "name": title, "description": desc, "provider": org, "areaServed": "Worldwide", "inLanguage": lang, "url": url}
    en = h.replace("</title>", "</title>\n" + headtags(url_en, title_en, desc_en, "en", ld_for("en", title_en, desc_en, url_en)), 1)
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(en)
    # --- Arabic static page
    soup = BeautifulSoup(h, "html.parser")
    for el in soup.select("[data-i18n]"):
        k = el.get("data-i18n")
        if k in ar:
            el.clear()
            for c in list(BeautifulSoup(ar[k], "html.parser").contents): el.append(c)
    soup.html["lang"] = "ar"; soup.html["dir"] = "rtl"
    h1 = soup.find("h1"); lead = soup.select_one(".lead")
    title_ar = ("درج — حيث يلتقي المال بالأعمال" if fname == "index.html" else (h1.get_text(" ", strip=True) + " | درج")) if h1 else "درج"
    desc_ar = lead.get_text(" ", strip=True) if lead else title_ar
    soup.title.string = title_ar
    soup.find("meta", attrs={"name": "description"})["content"] = desc_ar
    lb = soup.find(id="langBtn"); lb["href"] = f"../{fname}"; lb["hreflang"] = "en"; lb["lang"] = "en"; lb.string = "English"
    for a in soup.find_all("a", href=True):
        if a["href"].endswith(".pdf"): a["href"] = "../" + a["href"]
    for im in soup.find_all("img"):
        if im.get("src", "").startswith("images/"): im["src"] = "../" + im["src"]
        if im.get("data-alt-ar"): im["alt"] = im["data-alt-ar"]
    out_ar = str(soup).replace("</title>", "</title>\n" + headtags(url_ar, title_ar, desc_ar, "ar", ld_for("ar", title_ar, desc_ar, url_ar)), 1)
    open(os.path.join(OUT, "ar", fname), "w", encoding="utf-8").write(out_ar)
    SITEMAP += [url_en, url_ar]

for f in os.listdir(SRC):
    if f.endswith(".pdf"): shutil.copy(os.path.join(SRC, f), OUT)
shutil.copytree(os.path.join(SRC, "images"), os.path.join(OUT, "images"))
open(OUT + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in SITEMAP) + "</urlset>\n")
open(OUT + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("pages:", len(pages), "->", len(os.listdir(OUT)), "files +", len(os.listdir(OUT + "/ar")), "Arabic")
