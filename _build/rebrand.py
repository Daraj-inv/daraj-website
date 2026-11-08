# Apply the Daraj Brand Kit v1 to the built site in final/ (run after seo.py)
import os, re, shutil, json
from urllib.parse import quote
DOMAIN = "https://daraj-website.mohamed-elsayeed82.workers.dev"
WA_LINK = "https://wa.me/201002701704"
KIT = "/home/claude/brandkit_in/Daraj-Brand-Kit"; OUT = "final"
os.makedirs(f"{OUT}/brand", exist_ok=True)
for f in ["daraj-logo-horizontal-white-no-slogan.svg", "daraj-logo-horizontal-white.svg", "daraj-icon-white.svg"]:
    shutil.copy(f"{KIT}/01-logo/SVG/{f}", f"{OUT}/brand/{f}")
for f in os.listdir(f"{KIT}/03-website"):
    if f.startswith(("favicon", "apple-touch", "android-chrome", "site.webmanifest", "daraj-share-image")):
        shutil.copy(f"{KIT}/03-website/{f}", f"{OUT}/{f}")
HEX = {"#E3A93B": "#D4AD57", "#e3a93b": "#D4AD57", "#EDB955": "#DDBB6C", "#0F1E33": "#0E2342", "#16294A": "#16305A", "#B07A12": "#B8902F", "#F4E6C8": "#F1E6CC", "#1D3560": "#1E3E70"}
CSS = """
body{font-family:Montserrat,"IBM Plex Sans Arabic",system-ui,sans-serif}
h1,h2,h3,h4{font-family:Montserrat,"IBM Plex Sans Arabic",sans-serif;font-weight:600;letter-spacing:-.01em}
[dir=rtl] body,[dir=rtl] h1,[dir=rtl] h2,[dir=rtl] h3,[dir=rtl] h4{font-family:"IBM Plex Sans Arabic",Montserrat,sans-serif;letter-spacing:0}
.logo img{display:block;height:30px;width:auto}footer .logo img{height:46px}
.pathc .k{color:var(--goldd)}.pathc.g .k{color:var(--gold)}
.btn-gold:hover{background:#DDBB6C}
.slog{color:var(--gold);font-weight:600;font-size:16px;margin:14px 0 0}
"""
FONT = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap"
slugs = {}
exec(open("articles_data.py", encoding="utf-8").read())
for a in ARTICLES: slugs[a["slug"]] = a["img"]
n = 0
for d, pre in [(OUT, ""), (f"{OUT}/ar", "../")]:
    for f in os.listdir(d):
        if not f.endswith(".html"): continue
        p = os.path.join(d, f); h = open(p, encoding="utf-8").read()
        for a, b in HEX.items(): h = h.replace(a, b)
        h = re.sub(r'https://fonts\.googleapis\.com/css2\?family=Inter[^"]*', FONT, h)
        h = h.replace("Space Grotesk", "Montserrat").replace("Inter,", "Montserrat,")
        # logos: header (no slogan), footer (with slogan)
        logos = list(re.finditer(r'(<a [^>]*class="logo"[^>]*>)\s*<svg.*?</svg>\s*<b>Daraj</b>.*?(</a>)', h, re.S))
        for i, m in reversed(list(enumerate(logos))):
            src = "daraj-logo-horizontal-white.svg" if i == len(logos) - 1 and len(logos) > 1 else "daraj-logo-horizontal-white-no-slogan.svg"
            h = h[:m.start()] + m.group(1) + f'<img src="{pre}brand/{src}" alt="Daraj — Take the next step" width="{"182" if "no-slogan" in src else "210"}" height="{"36" if "no-slogan" in src else "56"}">' + m.group(2) + h[m.end():]
        # head: favicons, manifest, theme colour, share image
        head = (f'<link rel="icon" href="{pre}favicon.ico" sizes="any"><link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">'
                f'<link rel="apple-touch-icon" href="{pre}apple-touch-icon-180x180.png"><link rel="manifest" href="{pre}site.webmanifest"><meta name="theme-color" content="#0E2342">')
        h = re.sub(r'<link rel="icon"[^>]*>', "", h)
        h = h.replace("</head>", head + "\n</head>", 1)
        img = f"images/{slugs[f]}.jpg" if f in slugs else "daraj-share-image-1200x630.png"
        h = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', lambda m: m.group(1) + "https://daraj-website.mohamed-elsayeed82.workers.dev/" + img + m.group(2), h)
        if "og:image:width" not in h and img.endswith(".png"):
            h = h.replace('<meta property="og:image"', '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image"', 1)
        # WhatsApp: every chat button and the floating button open a chat with Daraj
        def wa_fix(m):
            tag = re.sub(r'href="[^"]*"', 'href="' + WA_LINK + '"', m.group(1))
            return tag.replace("<a ", '<a target="_blank" rel="noopener" ', 1) + m.group(2)
        h = re.sub(r'(<a\b[^>]*>)((?:Chat on WhatsApp|تواصل عبر واتساب)</a>)', wa_fix, h)
        h = re.sub(r'(<a\b[^>]*class="wa"[^>]*>)()', wa_fix, h)
        # article share buttons
        url = DOMAIN + "/" + ("ar/" if pre else "") + ("" if f == "index.html" else f)
        h = re.sub(r'(<a\b[^>]*)href="#"([^>]*>)WhatsApp</a>', lambda m: m.group(1) + 'href="https://wa.me/?text=' + quote(url) + '" target="_blank" rel="noopener"' + m.group(2) + "WhatsApp</a>", h)
        h = re.sub(r'(<a\b[^>]*)href="#"([^>]*>)LinkedIn</a>', lambda m: m.group(1) + 'href="https://www.linkedin.com/sharing/share-offsite/?url=' + quote(url, safe="") + '" target="_blank" rel="noopener"' + m.group(2) + "LinkedIn</a>", h)
        # footer contact: WhatsApp only (email and address stay private)
        h = re.sub(r'<span>\[email\]</span>\s*<span>\[WhatsApp\]</span>\s*<span>\[address\]</span>', '<a href="' + WA_LINK + '" target="_blank" rel="noopener" style="color:#fff;font-weight:600" dir="ltr">WhatsApp · +20 100 270 1704</a>', h)
        if pre:  # Arabic pages: the logo slogan is English, so add it in Arabic too
            h = re.sub(r'(<footer>.*?</nav>)', lambda m: m.group(1) + '<p class="slog">اتخذ الخطوة التالية.</p>', h, count=1, flags=re.S)
        h = h.replace("</style>", CSS + "</style>", 1)
        open(p, "w", encoding="utf-8").write(h); n += 1
print("rebranded", n, "pages")
