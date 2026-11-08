"""Shared builder for Jesr service pages (bilingual EN/AR, no prices, two-door nav, founder access, Majlis/Insights)."""
import json, re
exec(open("/tmp/bedaya_prefix.py", encoding="utf-8").read())   # t, AR, head (shared CSS), CHECK, LOGO
_ccss = open("/home/claude/brand/site/build_consult_page.py", encoding="utf-8").read()
EXTRA_CSS = _ccss[_ccss.index('head = head.replace("</style>", """') + len('head = head.replace("</style>", """'):_ccss.index('</style>""")')]
BASE_HEAD = head.replace("</style>", EXTRA_CSS + """
.founder{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.founder>div{background:var(--navy2);border-radius:18px;padding:26px;color:#fff;border-top:4px solid var(--gold)}
.founder .k{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
[dir=rtl] .founder .k{letter-spacing:0}
.founder h3{font-size:21px;margin:8px 0}.founder p{color:#C9D2DE;margin:0;font-size:15px}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;margin-top:28px}
.strip a{display:block;text-decoration:none;border:1px solid #2A3D5C;border-radius:18px;padding:24px;color:#fff}
.strip a:hover{border-color:var(--gold)}.strip h3{font-size:20px;color:var(--gold)}.strip p{margin:6px 0 0;color:#C9D2DE;font-size:15px}
.buyer{margin-top:18px;font-size:15px;color:var(--navy)}.buyer a{font-weight:700}
</style>""")

def nav_html(cur):
    def a(key, en, ar, href):
        return t(key, en, ar, "a", f'href="{href}"' + (' class="cur"' if key == cur else ""))
    return f"""<header>
  <div class="wrap hbar">
    <a class="logo" href="#top" aria-label="Jesr home">{LOGO}<b>Jesr</b><span class="ar">جسر</span></a>
    <nav class="main" aria-label="Main">
      {t("nav_home","Home","الرئيسية","a",'href="index.html" class="hide-m"')}
      <div class="dd"><button type="button" aria-haspopup="true">{t("nav_services","Services","الخدمات")} ▾</button>
        <div class="dd-menu">
          <div>{t("div_invest","Jesr Invest · money &amp; ownership","جسر للاستثمار · المال والملكية","h4")}{a("s_capital","Jesr Capital","جسر كابيتال","jesr-capital.html")}<br>{a("s_club","Investors Club","نادي المستثمرين","jesr-investors-club.html")}<br>{a("s_safqa","Jesr Safqa","جسر صفقة","jesr-safqa.html")}<br>{a("s_bedaya","Jesr Bedaya","جسر بداية","jesr-bedaya.html")}</div>
          <div>{t("div_bs","Jesr Business · fix &amp; grow","جسر للأعمال · إصلاح ونمو","h4")}{a("s_consult","Jesr Consulting","جسر للاستشارات","jesr-consulting.html")}<br>{a("s_depts","Jesr Departments","جسر للإدارات","jesr-departments.html")}<br>{a("s_adv","Private Advisory","الاستشارة الخاصة","jesr-departments.html#founder")}</div>
        </div></div>
      {t("nav_ins","Insights","رؤى جسر","a",'href="index.html#insights" class="hide-m"')}
      {t("nav_maj","Majlis","المجلس","a",'href="index.html#majlis" class="hide-m"')}
      <button class="lang" id="langBtn" type="button">العربية</button>
      {{CTA}}
    </nav>
  </div>
</header>"""

def founder_html(er_en, er_ar):
    return f"""<section class="dark" id="founder"><div class="wrap">
  <div class="sec-head">{t("fd_eyebrow","Founder-led","بقيادة المؤسس","div",'class="eyebrow"')}{t("fd_h2","Direct access to our founder.","تواصل مباشر مع مؤسسنا.","h2")}{t("fd_p","Jesr is led by an experienced business advisor who works with owners, CEOs and chairmen personally.","يقود جسر مستشار أعمال خبير يعمل شخصيًا مع أصحاب الأعمال والرؤساء التنفيذيين ورؤساء مجالس الإدارة.","p")}</div>
  <div class="founder">
    <div>{t("fd1k","Open door","باب مفتوح","div",'class="k"')}{t("fd1h","Founder-led first call","أول مكالمة مع المؤسس","h3")}{t("fd1p","For senior owners and decision-makers, your first call can be led by our founder.","لأصحاب الأعمال ومتخذي القرار، يمكن أن يقود مؤسسنا مكالمتك الأولى.","p")}</div>
    <div>{t("fd2k","Included","ضمن الخدمة","div",'class="k"')}{t("fd2h","Executive Review","المراجعة التنفيذية","h3")}{t("fd2p",f"A quarterly 1-to-1 strategy session with our founder. {er_en}",f"جلسة استراتيجية فردية كل ربع سنة مع مؤسسنا. {er_ar}","p")}</div>
    <div>{t("fd3k","Signature","مميزة","div",'class="k"')}{t("fd3h","Jesr Private Advisory","الاستشارة الخاصة من جسر","h3")}{t("fd3p","A personal business advisor to CEOs and chairmen. Limited places.","مستشار أعمال شخصي للرؤساء التنفيذيين ورؤساء مجالس الإدارة. أماكن محدودة.","p")}</div>
  </div>
  <div class="strip">
    <a href="index.html#majlis">{t("sx1h","Jesr Majlis","مجلس جسر","h3")}{t("sx1p","Our community: monthly sessions where owners, investors and entrepreneurs meet and do business.","مجتمعنا: جلسات شهرية يلتقي فيها أصحاب الأعمال والمستثمرون ورواد الأعمال ويعقدون الصفقات.","p")}</a>
    <a href="index.html#insights">{t("sx2h","Jesr Insights","رؤى جسر","h3")}{t("sx2p","Practical articles on growth, money, deals and AI with real numbers.","مقالات عملية عن النمو والمال والصفقات والذكاء الاصطناعي بأرقام حقيقية.","p")}</a>
  </div>
</div></section>"""

FOOT = lambda disc_en, disc_ar: f"""<footer><div class="wrap">
  <div class="fgrid2"><a class="logo" href="#top">{LOGO.replace('34','30')}<b>Jesr</b><span class="ar">جسر</span></a>
    <div style="display:flex;gap:28px;flex-wrap:wrap"><span>[email]</span><span>[WhatsApp]</span><span>[address]</span></div></div>
  {t("disc",disc_en,disc_ar,"p",'class="disc"')}
</div></footer>"""

SCRIPT = """<script>
const AR = __AR__;
const EN = {};
document.querySelectorAll("[data-i18n]").forEach(el => { const k = el.dataset.i18n; if (!(k in EN)) EN[k] = el.innerHTML; });
let lang = "en";
try { if (localStorage.getItem("jesr-lang") === "ar") lang = "ar"; } catch (e) {}
const qp = new URLSearchParams(location.search).get("lang"); if (qp === "ar" || qp === "en") lang = qp;
function applyLang() {
  const d = lang === "ar" ? AR : EN;
  document.documentElement.lang = lang; document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach(el => { const k = el.dataset.i18n; if (d[k] !== undefined) el.innerHTML = d[k]; });
  document.getElementById("langBtn").textContent = lang === "ar" ? "English" : "العربية";
  try { localStorage.setItem("jesr-lang", lang); } catch (e) {}
}
document.getElementById("langBtn").addEventListener("click", () => { lang = lang === "ar" ? "en" : "ar"; applyLang(); });
document.querySelectorAll("select").forEach(s => { if (s.options.length) s.options[0].value = ""; });
// form: connect to Google Sheets / a form service when the site goes live
const bf = document.getElementById("bookForm");
if (bf) bf.addEventListener("submit", e => { e.preventDefault(); bf.hidden = true; document.getElementById("thanks").hidden = false; });
applyLang();
</script>
</body>
</html>"""

def opts(k, items):
    return "".join(t(f"{k}{i}", a, b, "option", f'value="{i}"') for i, (a, b) in enumerate(items))

def field(k, en, ar, kind="text", name=None, items=None, full=False, req=True, attrs=""):
    name = name or k
    lab = t(k, en, ar)
    cls = ' class="full"' if full else ""
    rq = " required" if req else ""
    if kind == "select":
        return f'<label{cls}>{lab}<select{rq} name="{name}">{opts("o" + k, items)}</select></label>'
    if kind == "textarea":
        return f'<label{cls}>{lab}<textarea name="{name}" rows="2"></textarea></label>'
    return f'<label{cls}>{lab}<input{rq} name="{name}" type="{kind}" {attrs}></label>'

def page(P):
    """P: dict with keys cur, title, desc, cta(nav), hero, card, pain, steps, feat, cards, faq, form, related, er, disc"""
    AR.clear()
    h = P["hero"]
    nav = nav_html(P["cur"]).replace("{CTA}", t("nav_cta", P["cta"][0], P["cta"][1], "a", 'href="#start" class="btn btn-gold" style="padding:10px 18px;min-height:44px;font-size:15px"'))
    trust = "".join(f'<span>{CHECK}{t(f"tr{i}", a, b)}</span>' for i, (a, b) in enumerate(h["trust"]))
    pain = P["pain"]
    quotes = "".join(f'<div class="q"><span class="m">“</span>{t(f"q{i}", a, b, "p")}{t(f"q{i}s", c, d, "small")}</div>' for i, (a, b, c, d) in enumerate(pain["q"]))
    st = P["steps"]
    s6 = "".join(f'<div class="s6"><div class="n">0{i+1}</div>{t(f"st{i}", a, b, "h3")}{t(f"st{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(st["items"]))
    fe = P["feat"]
    a6 = "".join(f'<div class="{"ai" if i == fe.get("hl", -1) else ""}"><div class="n">0{i+1}</div>{t(f"fe{i}", a, b, "h3")}{t(f"fe{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(fe["items"]))
    cd = P["cards"]
    cards = "".join(f'<div>{t(f"cd{i}k", a, b, "div", "class=\"k\"")}{t(f"cd{i}h", c, d, "h3")}{t(f"cd{i}p", e, f, "p")}</div>' for i, (a, b, c, d, e, f) in enumerate(cd["items"]))
    fq = "".join(f'<details>{t(f"fq{i}", a, b, "summary")}{t(f"fa{i}", c, d, "p")}</details>' for i, (a, b, c, d) in enumerate(P["faq"]))
    fm = P["form"]
    csteps = "".join(f'<div class="step"><b>{i+1}</b><div>{t(f"cs{i}", a, b, "strong")}<br>{t(f"cs{i}p", c, d)}</div></div>' for i, (a, b, c, d) in enumerate(fm["steps"]))
    rel = "".join(f'<a class="rel" href="{href}">{t(f"rs{i}", a, b, "h3")}{t(f"rl{i}", c, d, "p")}</a>' for i, (href, a, b, c, d) in enumerate(P["related"]))
    body = f"""{nav}
<div class="crumb"><div class="wrap"><a href="#" data-i18n="nav_services">Services</a> / <span data-i18n="{P['door']}">{P['door_txt']}</span> / <span style="color:#fff" data-i18n="{P['cur']}">{P['cur_txt']}</span></div></div>
<section class="hero" id="top"><div class="wrap hero-grid">
  <div style="flex:1 1 520px">
    {t("hero_eyebrow", h["eyebrow"][0], h["eyebrow"][1], "div", 'class="eyebrow" style="color:var(--gold)"')}
    {t("hero_h1", h["h1"][0], h["h1"][1], "h1", 'style="font-size:clamp(38px,5.4vw,64px)"')}
    {t("hero_lead", h["lead"][0], h["lead"][1], "p", 'class="lead"')}
    <div class="ctas">{t("cta1", h["c1"][0], h["c1"][1], "a", 'class="btn btn-gold" href="#start"')}{t("cta2", h["c2"][0], h["c2"][1], "a", 'class="btn btn-line" href="#how" style="color:#fff"')}</div>
    <div class="trust">{trust}</div>
  </div>
  <div style="flex:1 1 360px">{P["card"]()}</div>
</div></section>
<section class="ivory"><div class="wrap">
  <div class="sec-head">{t("pain_eyebrow", *pain["eyebrow"], "div", 'class="eyebrow"')}{t("pain_h2", *pain["h2"], "h2")}</div>
  <div class="quotes">{quotes}</div>
  <div class="answer">{t("ans_h", *pain["ans_h"], "h3")}{t("ans_p", *pain["ans_p"], "p")}</div>
</div></section>
<section id="how"><div class="wrap">
  <div class="sec-head">{t("how_eyebrow", *st["eyebrow"], "div", 'class="eyebrow"')}{t("how_h2", *st["h2"], "h2")}{t("how_p", *st["p"], "p")}</div>
  <div class="steps6" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{s6}</div>
</div></section>
<section class="ivory"><div class="wrap">
  <div class="sec-head">{t("fe_eyebrow", *fe["eyebrow"], "div", 'class="eyebrow"')}{t("fe_h2", *fe["h2"], "h2")}{t("fe_p", *fe["p"], "p")}</div>
  <div class="areas6">{a6}</div>
</div></section>
<section><div class="wrap">
  <div class="sec-head">{t("cd_eyebrow", *cd["eyebrow"], "div", 'class="eyebrow"')}{t("cd_h2", *cd["h2"], "h2")}</div>
  <div class="sizes">{cards}</div>
</div></section>
{founder_html(*P["er"])}
<section class="ivory"><div class="wrap faq">
  <div class="sec-head">{t("faq_eyebrow","Questions people ask","أسئلة شائعة","div",'class="eyebrow"')}{t("faq_h2","Frequently asked questions","الأسئلة الشائعة","h2")}</div>
  {fq}
</div></section>
<section class="cta" id="start"><div class="wrap cta-grid">
  <div class="cta-txt">
    {t("cta_eyebrow", *fm["eyebrow"], "div", 'class="eyebrow" style="color:var(--navy)"')}
    {t("cta_h2", *fm["h2"], "h2")}
    {t("cta_lead", *fm["lead"], "p", 'class="lead"')}
    <div class="steps">{csteps}</div>
    {fm.get("extra", "")}
  </div>
  <div class="form">
    <form id="bookForm">
      {t("f_h", *fm["fh"], "h3")}
      <div class="fgrid">{"".join(fm["fields"])}
        <label class="full chk"><input type="checkbox" required name="consent">{t("consent", *fm["consent"])}</label>
      </div>
      {t("btn", *fm["btn"], "button", 'class="btn btn-navy" type="submit"')}
    </form>
    <div class="thanks" id="thanks" hidden>{t("thx_h","Thank you, we’ve received your request.","شكرًا لك، تم استلام طلبك.","h3")}{t("thx_p", *fm["thx"], "p")}</div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="sec-head">{t("rel_eyebrow","Related services","خدمات مرتبطة","div",'class="eyebrow"')}{t("rel_h2", *P["rel_h2"], "h2")}</div>
  <div class="related">{rel}</div>
</div></section>
{FOOT(*P["disc"])}
"""
    hd = re.sub(r"<title>.*?</title>", f"<title>{P['title']}</title>", BASE_HEAD)
    hd = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{P["desc"]}">', hd)
    # door + cur labels in crumb come from nav keys
    return hd.split("<body>")[0] + "<body>\n" + body + SCRIPT.replace("__AR__", json.dumps(AR, ensure_ascii=False))

def patch_existing(html, cur, er_en, er_ar, faq_anchor):
    """Give older generated pages (Bedaya, Consulting) the final nav, founder section and keys."""
    AR.clear()
    new_nav = nav_html(cur)
    m = re.search(r'<div class="dd-menu">.*?</div></div>', html, re.S)
    menu_new = re.search(r'<div class="dd-menu">.*?</div></div>', new_nav, re.S).group(0)
    html = html[:m.start()] + menu_new + html[m.end():]
    html = html.replace('<a href="#" class="hide-m" data-i18n="nav_home">Home</a>', '<a href="index.html" class="hide-m" data-i18n="nav_home">Home</a>')
    html = html.replace(faq_anchor, founder_html(er_en, er_ar) + "\n" + faq_anchor, 1)
    extra = json.dumps(AR, ensure_ascii=False)[1:-1]
    html = html.replace("const AR = {", "const AR = {" + extra + ",", 1)
    return html
