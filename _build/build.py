import re, json, os, shutil
exec(open("/home/claude/brand/site/pagekit.py", encoding="utf-8").read())   # t, AR, BASE_HEAD, nav_html, FOOT, SCRIPT, field, CHECK, LOGO
SRC = "/home/claude/final/website"
OUT = "/home/claude/daraj_web/site"

STEPS_LOGO = lambda n: f'<svg width="{n}" height="{n}" viewBox="0 0 36 36" aria-hidden="true"><rect x="2" y="22" width="9" height="12" rx="1.5" fill="#E3A93B"></rect><rect x="13.5" y="14" width="9" height="20" rx="1.5" fill="#E3A93B"></rect><rect x="25" y="4" width="9" height="30" rx="1.5" fill="#E3A93B"></rect></svg>'

EXTRA_CSS = """
.topbar{background:var(--gold);color:var(--navy);font-size:14px;font-weight:600;text-align:center;padding:9px 16px}
.topbar a{color:var(--navy);margin-inline-start:10px}
.wa{position:fixed;inset-inline-end:22px;bottom:22px;width:60px;height:60px;border-radius:50%;background:#1FA855;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 22px rgba(15,30,51,.3);z-index:60}
.pick{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px;margin-top:22px}
.pick a{display:block;text-decoration:none;color:#fff;background:var(--navy2);border:1px solid #2A3D5C;border-radius:16px;padding:22px 24px;transition:border-color .2s,transform .2s}
.pick a:hover{border-color:var(--gold);transform:translateY(-2px)}
.pick b{display:block;font-size:19px;font-family:"Space Grotesk",Inter,sans-serif}.pick span{display:block;color:#C9D2DE;font-size:14px;margin-top:6px}
.doors{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:22px}
.door{border-radius:22px;padding:38px;display:flex;flex-direction:column;gap:18px}
.door.n{background:var(--navy);color:#fff}.door.w{background:#fff;border:1px solid var(--line)}
.door h3{font-size:32px}.door .sub{margin:0;color:var(--muted)}.door.n .sub{color:#C9D2DE}
.door .rows a{display:flex;justify-content:space-between;gap:16px;padding:16px 0;border-top:1px solid var(--line);text-decoration:none;color:inherit}
.door.n .rows a{border-color:#2A3D5C}.door .rows a b{font-size:18px}.door .rows a span{color:var(--muted);font-size:15px;text-align:end}.door.n .rows a span{color:#C9D2DE}
.door .rows a:hover b{color:var(--goldd)}.door.n .rows a:hover b{color:var(--gold)}
.band{background:var(--gold);padding:52px 0}.band .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:22px}
.band h2{font-size:clamp(26px,3.4vw,36px);color:var(--navy)}.band p{margin:6px 0 0;color:var(--navy);font-size:17px}
.why{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.why>div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px}.why h3{font-size:20px;margin:12px 0 8px}.why p{margin:0;color:var(--muted)}
.tq{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.tq figure{margin:0;background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:18px;padding:46px 28px 28px;position:relative}.tq .smp{position:absolute;top:14px;inset-inline-end:16px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A7F6A;background:#F3EEE3;border-radius:20px;padding:3px 10px}.tq blockquote{margin:0 0 16px;font-size:18px}.tq figcaption{color:var(--muted);font-size:14px}
.ins{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}
.icard{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;color:var(--ink);transition:transform .2s,box-shadow .2s}
.icard:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(15,30,51,.12)}
.icard .im{height:160px;background:var(--navy);display:flex;align-items:flex-end;padding:20px}.icard:nth-child(even) .im{background:var(--navy2)}
.icard .bd{padding:24px;display:flex;flex-direction:column;gap:10px}.icard .cat{font-size:12px;font-weight:700;letter-spacing:.12em;color:var(--goldd);text-transform:uppercase}
[dir=rtl] .icard .cat{letter-spacing:0}.icard h3{font-size:21px;line-height:1.3}.icard p{margin:0;color:var(--muted);font-size:15px}.icard .meta{font-size:13px;color:var(--muted)}
.soon{display:inline-block;background:var(--goldl);color:var(--goldd);font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}
.pills{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px}.pills button{border:1px solid #C9C1B1;background:#fff;color:var(--ink);border-radius:999px;padding:10px 18px;font:inherit;font-size:14px;font-weight:600;cursor:pointer;min-height:44px}
.pills button.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.video{display:flex;flex-direction:column;justify-content:flex-end;gap:6px;min-height:320px;border-radius:20px;background:var(--navy);color:#fff;text-decoration:none;padding:26px}
.majcard{background:var(--navy);border:1px solid #2A3D5C;border-radius:20px;padding:30px;display:flex;flex-direction:column;gap:12px}
.split{display:flex;flex-wrap:wrap;gap:48px;align-items:center}.split>.a{flex:999 1 520px;min-width:0}.split>.b{flex:1 1 340px;min-width:0}
.prose{max-width:720px}.prose p{font-size:17px;line-height:1.8;margin:0 0 18px;color:#2A3442}.prose h2{font-size:24px;line-height:1.3;margin:38px 0 12px;scroll-margin-top:110px}
.prose blockquote{margin:28px 0;padding:24px 28px;background:var(--ivory);border-radius:14px;font-family:"Space Grotesk",Inter,sans-serif;font-size:20px;line-height:1.45;border-inline-start:4px solid var(--gold)}
.artw{display:flex;flex-wrap:wrap;gap:56px;align-items:flex-start}.artw .prose{flex:999 1 620px;min-width:0}.artw aside{flex:1 1 300px;min-width:0;position:sticky;top:110px;display:flex;flex-direction:column;gap:16px}
.side{background:var(--navy);color:#fff;border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:12px}.side p{margin:0;color:#C9D2DE}
.netw{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.netw>div{background:var(--navy2);border:1px solid #2A3D5C;border-radius:18px;padding:26px;color:#fff}.netw h3{font-size:20px;color:var(--gold);margin:0 0 8px}.netw p{margin:0;color:#C9D2DE}
@media (max-width:600px){.doors{grid-template-columns:1fr}.door{padding:26px}}
.icard>img{border-bottom:1px solid var(--line)}
.cover{margin:0;box-shadow:0 24px 60px rgba(15,30,51,.25);border-radius:20px}
.prose ul{margin:0 0 22px;padding-inline-start:24px}.prose li{font-size:17px;line-height:1.7;margin:6px 0}
.endcta{margin-top:40px;background:var(--navy);color:#fff;border-radius:22px;padding:34px;border-top:6px solid var(--gold)}
.endcta .k{color:var(--gold);font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase}[dir=rtl] .endcta .k{letter-spacing:0}
.endcta h2{color:#fff;font-size:24px;margin:10px 0 10px}.endcta p{color:#C9D2DE;font-size:17px;margin:0}.endcta .n{font-size:14px;margin-top:14px}
"""

WA_SVG = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.4-4.3a8.5 8.5 0 1 1 15.6-4.5z"></path></svg>'

def ar_of(html):
    m = re.search(r'const AR = (\{.*?\});\s*\nconst EN', html, re.S)
    return m, json.loads(m.group(1))

def set_ar(html, d):
    m, _ = ar_of(html)
    return html[:m.start(1)] + json.dumps(d, ensure_ascii=False) + html[m.end(1):]

def set_en(html, key, new):
    pat = re.compile(r'(data-i18n="' + re.escape(key) + r'"[^>]*>)(.*?)(</(?:span|p|h1|h2|h3|div|a|small|strong|summary|option|button|h4|b)>)', re.S)
    html2, n = pat.subn(lambda m: m.group(1) + new + m.group(3), html, count=1)
    assert n, key
    return html2

EXTRA_CSS += r'''
.acover{margin:0 0 28px}.acover img{display:block;width:100%;height:280px;object-fit:cover;border-radius:14px}
.ameta{display:flex;flex-wrap:wrap;gap:8px 18px;color:#C9D2DE;font-size:14px;margin-top:6px}
.tk{background:#fff;border:1px solid var(--line);border-inline-start:4px solid var(--gold);border-radius:14px;padding:20px 24px;margin:0 0 30px}
.tk b{display:block;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:8px}[dir=rtl] .tk b{letter-spacing:0}
.tk ul{margin:0;padding-inline-start:20px}.tk li{font-size:16px;margin:6px 0}
.atbl{margin:34px 0}.atbl h3{font-size:19px;margin:0 0 12px}.atbl .sc{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:#fff}
.atbl table{border-collapse:collapse;width:100%;font-size:15px;min-width:520px}.atbl th{background:var(--navy);color:#fff;text-align:start;padding:12px 14px;font-weight:600}
.atbl td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:top;line-height:1.55}.atbl tr td:first-child{font-weight:600;color:var(--navy)}.atbl tr:nth-child(even) td{background:#FAF7F0}
.aex{background:var(--ivory);border-radius:14px;padding:22px 24px;margin:34px 0}.aex .lb{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#8A6A1F;margin-bottom:8px}[dir=rtl] .aex .lb{letter-spacing:0}
.aex p{margin:0;font-size:16px}
.afaq{margin:38px 0 0}.afaq details{border-top:1px solid var(--line);padding:14px 0}.afaq details:last-child{border-bottom:1px solid var(--line)}
.afaq summary{cursor:pointer;font-weight:600;font-size:17px;color:var(--navy)}.afaq details p{margin:10px 0 0;font-size:16px}
.toc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px}.toc b{font-size:14px}.toc ol{margin:10px 0 0;padding-inline-start:18px}.toc li{font-size:14px;margin:7px 0;line-height:1.45}.toc a{color:var(--navy)}
.artw aside .side h3{font-size:19px!important}
@media(max-width:700px){.acover img{height:190px}.prose p,.prose li{font-size:16px}}
'''
EXTRA_CSS += r'''
.pstrip{background:var(--navy);color:#fff;padding:56px 0;border-top:4px solid var(--gold)}.pstrip .wrap{display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:center}
.pstrip .k{color:var(--gold);font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase}[dir=rtl] .pstrip .k{letter-spacing:0}.pstrip h2{color:#fff;margin:10px 0 8px;font-size:clamp(26px,3vw,36px)}.pstrip p{color:#C9D2DE;margin:0;max-width:640px;font-size:17px}
.paths{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.pathc{display:block;border-radius:20px;padding:30px;text-decoration:none;color:inherit;border:1px solid var(--line);background:#fff;transition:transform .2s}.pathc:hover{transform:translateY(-3px)}
.pathc.g{background:var(--navy);color:#fff;border-color:var(--navy)}.pathc.g p{color:#C9D2DE}.pathc .k{font-size:13px;font-weight:700;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}[dir=rtl] .pathc .k{letter-spacing:0}.pathc h3{font-size:24px;margin:10px 0}.pathc b{color:var(--gold)}
.aud{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}.aud div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px}
.aud .ic{width:46px;height:46px;border-radius:12px;background:var(--navy);color:var(--gold);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px;margin-bottom:14px}.aud h3{font-size:19px;margin:0 0 6px}.aud p{margin:0;color:var(--muted);font-size:15px}
.reality{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.reality div{border-inline-start:4px solid var(--gold);background:rgba(255,255,255,.05);border-radius:12px;padding:20px 22px}.reality h3{color:#fff;font-size:18px;margin:0 0 6px}.reality p{color:#C9D2DE;margin:0;font-size:15px}
.agent{background:#FBF4E3;border:1px solid #EBD9AE;border-radius:18px;padding:26px 30px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;margin-top:36px}.agent p{margin:0;font-size:18px;color:var(--navy);font-weight:600;max-width:760px}
.trustbox{display:flex;flex-wrap:wrap;gap:28px;align-items:center;background:var(--navy);color:#fff;border-radius:22px;padding:36px}.trustbox h2{color:#fff;margin:0 0 8px}.trustbox p{color:#C9D2DE;margin:0;font-size:17px;max-width:720px}
.heroaud{background:rgba(255,255,255,.06);border:1px solid #2A3D5C;border-radius:22px;padding:28px}.hlist{list-style:none;margin:16px 0 0;padding:0}.hlist li{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-top:1px solid #2A3D5C}.hlist li:first-child{border-top:0}.hlist svg{flex:0 0 auto;margin-top:3px}.hlist strong{display:block;color:#fff;font-size:16px}.hlist span{color:#C9D2DE;font-size:14px}
'''
def brand(html):
    html = html.replace(' (قريبًا)', '').replace('(قريبًا)', '').replace(' (soon)', '').replace(' (coming soon)', '')
    html = re.sub(r'jesr-([a-z-]+)\.html', r'daraj-\1.html', html)
    html = html.replace("jesr-lang", "daraj-lang")
    html = re.sub(r'<svg width="(\d+)" height="\1" viewBox="0 0 24 24" fill="none" stroke="#E3A93B" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M2 18h20"/><path d="M5 18v-6"/><path d="M19 18v-6"/><path d="M12 18v-8"/><path d="M2 12c4-6 16-6 20 0"/></svg>',
                  lambda m: STEPS_LOGO(int(m.group(1))), html)
    html = html.replace("ننظر في فريقك وحجم عملك.", "نراجع فريقك وحجم أعمالك.")
    html = html.replace("Jesr", "Daraj").replace("JESR", "DARAJ").replace("جسر", "درج")
    html = html.replace('href="index.html#insights"', 'href="daraj-insights.html"')
    html = html.replace('daraj-departments.html#founder', 'daraj-departments.html#senior').replace('id="founder"', 'id="senior"')
    html = html.replace('class="logo" href="#top"', 'class="logo" href="index.html"')
    html = html.replace('href="#" data-i18n="nav_services"', 'href="index.html#doors" data-i18n="nav_services"')
    if ".topbar{" not in html:
        html = html.replace("</style>", EXTRA_CSS + "</style>", 1)
    return html

def chrome(html):
    """Founding Period bar + floating WhatsApp, both bilingual."""
    m, d = ar_of(html)
    d.update({"tb_t": "فترة التأسيس متاحة الآن، ويحظى العملاء الأوائل بأولوية الاهتمام من كبار خبرائنا.", "tb_a": "احجز مكالمتك المجانية", "wa_l": "تواصل معنا عبر واتساب"})
    html = set_ar(html, d)
    bar = '<div class="topbar"><span data-i18n="tb_t">Founding Period now open. Early clients get priority attention from our senior team.</span><a href="#start" data-i18n="tb_a">Book your free call</a></div>'
    if 'class="topbar"' not in html:
        html = html.replace("<body>\n", "<body>\n" + bar + "\n", 1)
        html = html.replace("\n<script>\nconst AR", f'\n<a class="wa" href="#start" aria-label="Chat with us on WhatsApp">{WA_SVG}</a>\n<script>\nconst AR', 1)
    return html

SENIOR = {
 "fd_eyebrow": ("Senior access", "خبراء على أعلى مستوى"),
 "fd_h2": ("Experienced people on every case.", "خبراء متمرسون في كل مشروع."),
 "fd_p": ("Every client works with senior advisors from the first call, and our most important clients get more.", "يعمل كل عميل مع مستشارين ذوي خبرة منذ المكالمة الأولى، ويحظى كبار عملائنا بخدمات إضافية."),
 "fd1h": ("Senior-led first call", "المكالمة الأولى مع أحد كبار المستشارين"),
 "fd1p": ("Your first call is with a senior advisor who has direct experience of what you want to do.", "تكون مكالمتك الأولى مع مستشار يتمتع بخبرة مباشرة في مجال احتياجك."),
}
def unfounder(html):
    m, d = ar_of(html)
    for k, (en, ar) in SENIOR.items():
        if k in d:
            html = set_en(html, k, en); d[k] = ar
    if "fd2p" in d:
        html = html.replace("strategy session with our founder.", "strategy session with a senior partner.")
        d["fd2p"] = d["fd2p"].replace("مع مؤسسنا.", "مع أحد كبار الشركاء.")
    if "cs1p" in d and "مؤسس" in d["cs1p"]:
        html = set_en(html, "cs1p", "A free call with a senior advisor."); d["cs1p"] = "مكالمة مجانية مع أحد كبار المستشارين."
    if d.get("q1s") == "المؤسس المتعب": d["q1s"] = "صاحب المشروع المتعب"; html = set_en(html, "q1s", "The tired owner")
    return set_ar(html, d)

def club(html):
    m, d = ar_of(html)
    html = set_en(html, "hero_lead", "More than deals: a network. Reviewed opportunities, other serious investors to work with, and research in any country you choose. Relationships first, then deals.")
    d["hero_lead"] = "أكثر من صفقات: شبكة علاقات. فرص تمت مراجعتها، ومستثمرون جادون تعمل معهم، وأبحاث في أي دولة تختارها. العلاقات أولًا، ثم الصفقات."
    AR.clear()
    items = [("Investors meet investors", "شبكة تجمع المستثمرين", "Verified members meet at the Daraj Majlis and through private introductions.", "يلتقي الأعضاء الموثقون في مجلس درج ومن خلال تعارف خاص."),
             ("Co-invest together", "استثمروا معًا", "Join forces with investors who share your goals, sectors and ticket size.", "استثمر جنبًا إلى جنب مع مستثمرين يشاركونك الأهداف والقطاعات وحجم الاستثمار."),
             ("Search in any country", "بحث في أي دولة", "Tell us the market you want. We research it, find the opportunities and check them on the ground.", "حدّد السوق الذي تستهدفه، وسندرسه ونبحث عن الفرص ونتحقق منها ميدانيًا."),
             ("Relationships that last", "علاقات تدوم", "One relationship manager who knows you, your goals and your network.", "مدير علاقة واحد يعرفك ويعرف أهدافك وشبكتك.")]
    cards = "".join(f'<div>{t(f"nw{i}h", a, b, "h3")}{t(f"nw{i}p", c, e, "p")}</div>' for i, (a, b, c, e) in enumerate(items))
    sec = f'''<section class="dark" id="network" style="background:var(--navy);color:#fff"><div class="wrap">
  <div class="sec-head">{t("nw_eb","Open connections","علاقات مفتوحة","div",'class="eyebrow"')}{t("nw_h2","Your network is part of your return.","شبكة علاقاتك جزء من عائدك.","h2")}{t("nw_p","The best deals often come from the right people. The Club is built around relationships, not listings.","أفضل الصفقات تأتي غالبًا من الأشخاص المناسبين. النادي مبني على العلاقات، لا على قوائم العروض.","p",'style="color:#C9D2DE"')}</div>
  <div class="netw">{cards}</div>
  <div style="margin-top:28px">{t("nw_cta","Tell us where you want to invest →","حدّد وجهتك الاستثمارية ←","a",'class="btn btn-gold" href="#start"')}</div>
</div></section>
'''
    i = html.index('<section class="dark" id="senior">')
    html = html[:i] + sec + html[i:]
    fq = f'<details>{t("fqx1","Can you find opportunities in a specific country?","هل يمكنكم إيجاد فرص في دولة محددة؟","summary")}{t("fax1","Yes. Tell us the country, sector and ticket size. We research the market, search for opportunities and check them before you see them.","نعم. أخبرنا بالدولة والقطاع وحجم الاستثمار، فنبحث السوق ونجد الفرص ونتحقق منها قبل أن تراها.","p")}</details><details>{t("fqx2","Will I meet other investors?","هل سألتقي بمستثمرين آخرين؟","summary")}{t("fax2","Yes. Members meet other verified investors at the Daraj Majlis and through introductions, to share deals and co-invest.","نعم. يلتقي الأعضاء بمستثمرين موثقين آخرين في مجلس درج ومن خلال التعارف، لتبادل الصفقات والاستثمار المشترك.","p")}</details>'
    i = html.index("<details>")
    html = html[:i] + fq + html[i:]
    fld = f'<label class="full">{t("f_cty","Countries you want to invest in","الدول التي تريد الاستثمار فيها")}<input name="countries" type="text"></label>'
    i = html.index('<label class="full chk">')
    html = html[:i] + fld + html[i:]
    d.update(AR)
    upd = {"pain_h2": ("Good opportunities are rare. The right people are rarer.", "الفرص الجيدة نادرة، والأشخاص المناسبون أندر."),
           "q1": ("I want to invest in a specific country, but I don’t know the market.", "أريد الاستثمار في دولة محددة، لكني لا أعرف السوق."),
           "q1s": ("The global investor", "المستثمر الدولي"),
           "q2": ("I’d rather invest alongside people I trust.", "أفضّل أن أستثمر مع أشخاص أثق بهم."),
           "q2s": ("The co-investor", "المستثمر الشريك"),
           "ans_p": ("We bring you reviewed opportunities, connect you with investors who share your goals, search and research any market you choose, and stay with you after you invest.", "نقدم لك فرصًا تمت مراجعتها، ونربطك بمستثمرين يشاركونك أهدافك، ونبحث ونَدرس أي سوق تختاره، ونبقى معك بعد الاستثمار."),
           "st2": ("Tell us where to look", "أخبرنا أين نبحث"),
           "st2p": ("A country, a sector, a ticket size: we search and research it for you.", "سواء كانت دولة أو قطاعًا أو حجم استثمار محددًا، نتولى البحث والدراسة نيابةً عنك."),
           "fe1": ("Country search and research", "بحث ودراسة في أي دولة"),
           "fe1p": ("Pick a country and we research the market, find the opportunities and check them.", "اختر دولة، فنَدرس السوق ونجد الفرص ونتحقق منها."),
           "fe3": ("Investor-to-investor network", "شبكة تربط المستثمرين ببعضهم"),
           "fe3p": ("Meet verified investors at the Daraj Majlis, share deals and co-invest.", "التقِ بمستثمرين موثقين في مجلس درج، وتبادل الصفقات واستثمر معهم.")}
    for k, (en, ar) in upd.items():
        if k in d:
            html = set_en(html, k, en); d[k] = ar
        else:
            print("club key missing", k)
    return set_ar(html, d)

CAP_Q = {
 "consulting": [("f_rev","rev","Company annual revenue (USD)","الإيرادات السنوية للشركة (بالدولار الأمريكي)",
     [("$0 – no revenue yet (business not started)","صفر – لا توجد إيرادات بعد (النشاط لم يبدأ)"),("Less than $250,000","أقل من ٢٥٠ ألف دولار"),("$250,000 – $1 million","من ٢٥٠ ألفًا إلى مليون دولار"),("$1 – 5 million","من مليون إلى ٥ ملايين دولار"),("$5 – 20 million","من ٥ إلى ٢٠ مليون دولار"),("More than $20 million","أكثر من ٢٠ مليون دولار")]),
   ("f_bud","budget","Budget available for this project (USD)","الميزانية المتاحة لهذا المشروع (بالدولار الأمريكي)",
     [("Less than $5,000","أقل من ٥ آلاف دولار"),("$5,000 – 15,000","من ٥ إلى ١٥ ألف دولار"),("$15,000 – 50,000","من ١٥ إلى ٥٠ ألف دولار"),("More than $50,000","أكثر من ٥٠ ألف دولار"),("Not decided yet","لم تُحدد بعد")])],
 "departments": [("f_rev","rev","Company annual revenue (USD)","الإيرادات السنوية للشركة (بالدولار الأمريكي)",
     [("$0 – no revenue yet (business not started)","صفر – لا توجد إيرادات بعد (النشاط لم يبدأ)"),("Less than $250,000","أقل من ٢٥٠ ألف دولار"),("$250,000 – $1 million","من ٢٥٠ ألفًا إلى مليون دولار"),("$1 – 5 million","من مليون إلى ٥ ملايين دولار"),("$5 – 20 million","من ٥ إلى ٢٠ مليون دولار"),("More than $20 million","أكثر من ٢٠ مليون دولار")]),
   ("f_bud","budget","Monthly budget available for outsourced departments (USD)","الميزانية الشهرية المتاحة لإسناد الإدارات (بالدولار الأمريكي)",
     [("Less than $2,000","أقل من ألفي دولار"),("$2,000 – 5,000","من ألفين إلى ٥ آلاف دولار"),("$5,000 – 15,000","من ٥ إلى ١٥ ألف دولار"),("More than $15,000","أكثر من ١٥ ألف دولار"),("Not decided yet","لم تُحدد بعد")])],
}
def rev_zero(html):
    m, d = ar_of(html); AR.clear()
    o = t("ofl_revz", "$0 – no revenue yet (business not started)", "صفر – لا توجد إيرادات بعد (النشاط لم يبدأ)", "option", 'value="z"')
    html = html.replace('data-i18n="ofl_rev0">Choose</option>', 'data-i18n="ofl_rev0">Choose</option>' + o, 1)
    d.update(AR)
    return set_ar(html, d)
def capital(html, kind):
    m, d = ar_of(html); AR.clear()
    flds = ""
    for key, name, en, ar, opts in CAP_Q[kind]:
        o = t(f"{key}o0", "Choose", "اختر", "option", 'value=""') + "".join(t(f"{key}o{n+1}", e, r, "option", f'value="{n+1}"') for n, (e, r) in enumerate(opts))
        flds += f'<label>{t(key, en, ar, "span")}<select required name="{name}">{o}</select></label>'
    note = t("f_capn", "These questions help us prepare the right team for your call. Your answers stay confidential.", "تساعدنا هذه الأسئلة على تجهيز الفريق المناسب لمكالمتك، وتبقى إجاباتك سرية.", "p", 'class="full" style="margin:-4px 0 0;font-size:13px;color:var(--muted)"')
    i = html.index('<label class="full chk">')
    html = html[:i] + flds + note + html[i:]
    d.update(AR)
    return set_ar(html, d)

SVC_TQ = {
 "capital": [("Investors kept asking for numbers we didn’t have ready. Daraj built our valuation range and investor file, and within months we were negotiating with two serious partners.", "كان المستثمرون يطلبون أرقامًا لم نكن قد جهزناها. أعدّ درج نطاق التقييم وملف المستثمرين، وخلال أشهر كنا نتفاوض مع شريكين جادين.", "Founder · Manufacturing company", "مؤسس · شركة تصنيع"),
             ("We didn’t only need money. We needed someone who opens doors. The partner Daraj introduced brought us a new market as well as capital.", "لم نكن نحتاج إلى المال فقط، بل إلى من يفتح لنا الأبواب. والشريك الذي عرّفنا به درج جلب لنا سوقًا جديدة إلى جانب التمويل.", "Managing director · Logistics business", "مدير عام · شركة لوجستية"),
             ("Everything stayed confidential until we were ready. Our team and customers heard about the deal only when it was signed.", "بقي كل شيء سريًا حتى أصبحنا مستعدين، ولم يعلم فريقنا وعملاؤنا بالصفقة إلا بعد توقيعها.", "Owner · Healthcare group", "مالك · مجموعة رعاية صحية")],
 "club": [("Every opportunity I received had already been checked. For the first time I could compare deals on facts, not promises.", "كل فرصة وصلتني كانت قد خضعت للفحص مسبقًا، ولأول مرة استطعت المقارنة بين الصفقات بناءً على الحقائق لا الوعود.", "Private investor", "مستثمر خاص"),
          ("I wanted to invest in a country I didn’t know. The team researched the market and showed me three real businesses on the ground.", "أردت الاستثمار في دولة لا أعرفها، فدرس الفريق السوق وعرض عليّ ثلاثة مشاريع حقيقية على أرض الواقع.", "Family office investor", "مستثمر · مكتب عائلي"),
          ("The relationships are the real value. I now co-invest with two members I met at the Daraj Majlis.", "العلاقات هي القيمة الحقيقية؛ فأنا اليوم أستثمر مع عضوين تعرّفت عليهما في مجلس درج.", "Investor · Investors Club member", "مستثمر · عضو نادي المستثمرين")],
 "safqa": [("My biggest fear was my staff finding out. The listing never showed our name, and only verified buyers saw the details.", "كان أكبر مخاوفي أن يعلم موظفيّ بالأمر، لكن العرض لم يُظهر اسمنا أبدًا، ولم يطّلع على التفاصيل إلا مشترون موثقون.", "Owner · Restaurant group", "مالك · مجموعة مطاعم"),
           ("Many people had asked me “how much?”. Daraj brought buyers who could actually pay, and a price supported by the numbers.", "سألني كثيرون «كم السعر؟»، لكن درج جاء بمشترين قادرين على الدفع فعلًا، وبسعر تدعمه الأرقام.", "Founder · Retail business", "مؤسس · نشاط تجزئة"),
           ("They prepared the sale file properly before going to market. The buyer’s questions were already answered.", "أعدّوا ملف البيع باحتراف قبل طرحه في السوق، فكانت إجابات أسئلة المشتري جاهزة مسبقًا.", "Owner · Services company", "مالك · شركة خدمات")],
 "bedaya": [("I had savings and an idea everyone loved. The numbers showed a better option in my own field. I kept my job and the business is now profitable.", "كانت لديّ مدخرات وفكرة أعجبت الجميع، لكن الأرقام أظهرت خيارًا أفضل في مجال تخصصي. احتفظت بوظيفتي، والمشروع اليوم يحقق أرباحًا.", "Employee turned business owner", "موظف أصبح صاحب مشروع"),
            ("They didn’t just give me a plan. They stayed with me through setup, hiring and the first months after launch.", "لم يكتفوا بتقديم خطة، بل رافقوني في التأسيس والتوظيف والأشهر الأولى بعد الإطلاق.", "Founder · Food business", "مؤسسة · مشروع أغذية"),
            ("The money stayed in my company account at all times. That trust made every decision easier.", "بقيت أموالي في حساب شركتي طوال الوقت، وهذه الثقة جعلت كل قرار أسهل.", "First-time founder", "مؤسس لأول مرة")],
 "consult": [("The Business X-Ray found in one hour what we had missed for two years: the problem was cash collection, not sales.", "كشفت أشعة الأعمال في ساعة واحدة ما فاتنا لعامين: المشكلة كانت في التحصيل لا في المبيعات.", "CEO · Distribution company", "رئيس تنفيذي · شركة توزيع"),
             ("Other consultants left us a report. Daraj stayed until the changes worked, and measured the results at 30, 60 and 90 days.", "ترك لنا مستشارون آخرون تقريرًا فقط، أما درج فبقي معنا حتى نجحت التغييرات، وقاس النتائج بعد ٣٠ و٦٠ و٩٠ يومًا.", "Owner · Manufacturing business", "مالك · نشاط صناعي"),
             ("Automating our invoices and follow-ups saved our team hours every week.", "أتمتة الفواتير والمتابعات وفّرت على فريقنا ساعات كل أسبوع.", "Operations manager · Clinic group", "مدير العمليات · مجموعة عيادات")],
 "depts": [("I used to do the books on weekends. Now I receive a clear monthly report and spend my time on customers.", "كنت أعدّ الحسابات في عطلات نهاية الأسبوع، واليوم يصلني تقرير شهري واضح وأتفرغ لعملائي.", "Founder · Trading company", "مؤسس · شركة تجارية"),
           ("We started with finance, then added marketing and HR. It feels like having a full team for the cost of one hire.", "بدأنا بالمالية ثم أضفنا التسويق والموارد البشرية، وكأن لدينا فريقًا كاملًا بتكلفة موظف واحد.", "Managing director · Growing SME", "مدير عام · منشأة صغيرة ومتوسطة"),
           ("Nobody owned our IT and systems before. Now there is a plan, a monthly review and someone accountable.", "لم يكن أحد مسؤولًا عن تقنية المعلومات والأنظمة لدينا، واليوم توجد خطة ومراجعة شهرية وشخص مسؤول.", "Owner · Services company", "مالك · شركة خدمات")],
}
SMPA = 'class="smp"'; EBA = 'class="eyebrow"'
def tq_section(p, items, cls=""):
    figs = "".join(f'<figure>{t(f"{p}sm{i}", "Sample", "نموذج", "span", SMPA)}<blockquote>{t(f"{p}{i}", "“" + a + "”", "«" + b + "»")}</blockquote><figcaption>{t(f"{p}{i}n", c, d)}</figcaption></figure>' for i, (a, b, c, d) in enumerate(items))
    return f'<section{cls} id="testimonials"><div class="wrap"><div class="sec-head">{t(p+"eb","In their words","بكلماتهم","div",EBA)}{t(p+"h2","What our clients say.","ماذا يقول عملاؤنا.","h2")}</div><div class="tq">{figs}</div></div></section>\n'
SVC_TQ["private"] = [("Having a senior advisor I can call before any big decision has changed how I run the company. It is the second opinion I never had.", "وجود مستشار من كبار الخبراء أتصل به قبل أي قرار كبير غيّر طريقة إدارتي للشركة؛ إنه الرأي الثاني الذي لم يكن متاحًا لي من قبل.", "Chairman · Family business group", "رئيس مجلس إدارة · مجموعة شركات عائلية")]
def add_tq(html, key):
    m, d = ar_of(html); AR.clear()
    mm = re.search(r'<section( class="ivory")?><div class="wrap faq', html)
    sec = tq_section("stq", SVC_TQ[key], "" if mm.group(1) else ' class="ivory"')
    html = html[:mm.start()] + sec + html[mm.start():]
    d.update(AR)
    return set_ar(html, d)
TQ_FILE = {"jesr-capital.html": "capital", "jesr-investors-club.html": "club", "jesr-safqa.html": "safqa", "jesr-bedaya.html": "bedaya", "jesr-consulting.html": "consult", "jesr-departments.html": "depts"}

# ---------- 1. existing service pages ----------
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".html"): continue
    h = open(os.path.join(SRC, f), encoding="utf-8").read()
    h = brand(h); h = unfounder(h); h = chrome(h)
    if "investors-club" in f: h = club(h)
    if f == "jesr-consulting.html": h = capital(h, "consulting")
    if f == "jesr-capital.html": h = rev_zero(h)
    if f in TQ_FILE: h = add_tq(h, TQ_FILE[f])
    if f == "jesr-departments.html": h = capital(h, "departments")
    open(os.path.join(OUT, f.replace("jesr-", "daraj-")), "w", encoding="utf-8").write(h)
for f in os.listdir(SRC):
    if f.endswith(".pdf"): shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f.replace("Jesr", "Daraj")))
print("service pages done")

# ---------- 2. new pages in the same design system ----------
AW = lambda: '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"></svg>'
def arrow_en(s): return s + " →"
def L(en, ar): return (en, ar)

def nav_cta(): return t("nav_cta", "Free call", "مكالمة مجانية", "a", 'href="#start" class="btn btn-gold" style="padding:10px 18px;min-height:44px;font-size:15px"')

def contact_form(prefix, h2, lead, steps, fields, btn_txt, thx):
    cs = "".join(f'<div class="step"><b>{i+1}</b><div>{t(f"{prefix}cs{i}", a, b, "strong")}<br>{t(f"{prefix}cs{i}p", c, d)}</div></div>' for i, (a, b, c, d) in enumerate(steps))
    return f'''<section class="cta" id="start"><div class="wrap cta-grid">
  <div class="cta-txt">
    {t(prefix+"cta_eb","Free · no obligation","مجانًا · بدون أي التزام","div",'class="eyebrow" style="color:var(--navy)"')}
    {t(prefix+"cta_h2", *h2, "h2")}
    {t(prefix+"cta_lead", *lead, "p", 'class="lead"')}
    <div class="steps">{cs}</div>
  </div>
  <div class="form">
    <form id="bookForm">
      {t(prefix+"f_h","Book your free call","احجز مكالمتك المجانية","h3")}
      <div class="fgrid">{"".join(fields)}
        <label class="full chk"><input type="checkbox" required name="consent">{t(prefix+"consent","I agree that Daraj may contact me by WhatsApp and email.","أوافق على أن يتواصل معي درج عبر واتساب والبريد الإلكتروني.")}</label>
      </div>
      {t(prefix+"btn", *btn_txt, "button", 'class="btn btn-navy" type="submit"')}
    </form>
    <div class="thanks" id="thanks" hidden>{t("thx_h","Thank you, we’ve received your request.","شكرًا لك، تم استلام طلبك.","h3")}{t("thx_p", *thx, "p")}</div>
  </div>
</div></section>'''

GOAL_ITEMS = [("Raise capital or find a partner","تمويل مشروعي أو إيجاد شريك"),("Invest or connect with investors","الاستثمار أو التواصل مع المستثمرين"),("Sell my business","بيع مشروعي"),("Start a business","بدء مشروع جديد"),("Fix and grow my business","إصلاح مشروعي وتنميته"),("Have a team run my departments","إدارة أقسام مشروعي عبر فريق متخصص"),("Not sure yet","لست متأكدًا بعد")]
def basic_fields(p):
    return [field(p+"fn","Full name","الاسم الكامل"), field(p+"fw","WhatsApp number","رقم واتساب","tel"), field(p+"fe","Email","البريد الإلكتروني","email"), field(p+"fc","Country","الدولة"),
            field(p+"fg","I want to…","أريد أن…","select", items=[("Choose","اختر")] + GOAL_ITEMS, full=True)]
STD_STEPS = [("Tell us the basics","أخبرنا بالأساسيات","Two minutes, nothing to prepare.","دقيقتان فقط، دون أي تحضير."),("Talk to a senior advisor","تحدّث مع أحد كبار المستشارين","Sixty minutes, free, no obligation.","ستون دقيقة مجانًا ودون أي التزام."),("Get your next step in writing","خطوتك التالية موثقة كتابيًا","Clear, honest and yours to keep.","واضحة وصريحة ومحددة.")]
THX = ("We’ll contact you on WhatsApp within one working day.", "سنتواصل معك عبر واتساب خلال يوم عمل واحد.")

def band(p, h, sub, href="#start"):
    return f'''<section class="band"><div class="wrap"><div>{t(p+"bh", *h, "h2")}{t(p+"bp", *sub, "p")}</div>
<div class="ctas" style="margin:0">{t(p+"bb","Book a free call","احجز مكالمة مجانية","a",f'class="btn btn-navy" href="{href}"')}{t(p+"bw","Chat on WhatsApp","تواصل عبر واتساب","a",f'class="btn btn-line" href="{href}" style="border-color:var(--navy);color:var(--navy)"')}</div></div></section>'''

def build(fname, cur, title, desc, body, disc=("Daraj is an introduction, advisory and management services company. It never holds client funds and does not guarantee any investment or result.", "درج شركة متخصصة في الربط الاستثماري والاستشارات والخدمات الإدارية، لا تحتفظ بأموال العملاء ولا تضمن أي استثمار أو نتيجة."), extra_js=""):
    nav = nav_html(cur).replace("{CTA}", nav_cta())
    foot = FOOT(*disc)
    hd = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", BASE_HEAD)
    hd = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', hd)
    html = hd.split("<body>")[0] + "<body>\n" + nav + "\n" + body + "\n" + foot + "\n" + SCRIPT.replace("__AR__", json.dumps(AR, ensure_ascii=False))
    if extra_js: html = html.replace("</body>", extra_js + "\n</body>")
    if '<div id="start"></div>' in body: html = html.replace('href="#start"', 'href="index.html#start"')
    html = brand(html); html = chrome(html)
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)

HERO_SVG = '<svg viewBox="0 0 420 320" width="100%" style="max-width:420px;display:block;margin-inline:auto" aria-hidden="true"><rect x="10" y="230" width="90" height="80" rx="6" fill="#16294A"></rect><rect x="110" y="170" width="90" height="140" rx="6" fill="#16294A"></rect><rect x="210" y="105" width="90" height="205" rx="6" fill="#16294A"></rect><rect x="310" y="35" width="90" height="275" rx="6" fill="#1D3560"></rect><polyline points="55,230 155,170 255,105 355,35" fill="none" stroke="#E3A93B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></polyline><circle cx="55" cy="230" r="8" fill="#E3A93B"></circle><circle cx="155" cy="170" r="8" fill="#E3A93B"></circle><circle cx="255" cy="105" r="8" fill="#E3A93B"></circle><circle cx="355" cy="35" r="11" fill="#E3A93B"></circle></svg>'

SVC = {
 "capital": ("daraj-capital.html", "Daraj Capital", "درج كابيتال", "Grow your business with the right partner", "نمِّ مشروعك مع الشريك المناسب"),
 "club": ("daraj-investors-club.html", "Investors Club", "نادي المستثمرين", "Where smart money meets real business", "حيث يلتقي المال الذكي بالمشاريع الحقيقية"),
 "safqa": ("daraj-safqa.html", "Daraj Safqa", "درج صفقة", "The smart way to sell your business", "الطريقة الذكية لبيع مشروعك"),
 "bedaya": ("daraj-bedaya.html", "Daraj Bedaya", "درج بداية", "From idea to profit", "من الفكرة إلى الربحية"),
 "consult": ("daraj-consulting.html", "Daraj Consulting", "درج للاستشارات", "We stay and make it happen", "نبقى معك حتى يتحقق التغيير"),
 "depts": ("daraj-departments.html", "Daraj Departments", "درج للإدارات", "A full department. One monthly fee.", "إدارة كاملة. برسوم شهرية واحدة."),
 "private": ("daraj-private-advisory.html", "Daraj Private Advisory", "درج للاستشارات الخاصة", "Your private business manager", "مدير أعمالك الخاص"),
}

# ===== HOME =====
AR.clear()
chips = [("capital","Raise capital or find a partner","تمويل مشروعي أو إيجاد شريك"),("club","Invest or connect with investors","الاستثمار أو التواصل مع المستثمرين"),("safqa","Sell my business","بيع مشروعي"),("bedaya","Start a business","بدء مشروع جديد"),("consult","Fix and grow my business","إصلاح مشروعي وتنميته"),("depts","Have a team run my departments","إدارة أقسام مشروعي عبر فريق متخصص")]
chip_html = "".join(f'<a href="{SVC[k][0]}">{t(f"ch{i}", en+" →", ar+" ←", "b")}{t(f"ch{i}s", SVC[k][1]+" · "+SVC[k][3], SVC[k][2]+" · "+SVC[k][4])}</a>' for i, (k, en, ar) in enumerate(chips))
def door(cls, key, title, sub, rows, btn_label, href, btn_cls):
    r = "".join(f'<a href="{SVC[k][0]}">{t(f"{key}r{i}", SVC[k][1], SVC[k][2], "b")}{t(f"{key}r{i}s", SVC[k][3]+" →", SVC[k][4]+" ←")}</a>' for i, k in enumerate(rows))
    return f'<div class="door {cls}">{t(key+"h", *title, "h3")}{t(key+"s", *sub, "p", "class=\"sub\"")}<div class="rows">{r}</div><div>{t(key+"b", *btn_label, "a", f"class=\"btn {btn_cls}\" href=\"{href}\"")}</div></div>'
why = [("We never touch your money","لا نلمس أموالك أبدًا","Funds move directly between the parties, under contracts both sides sign.","تنتقل الأموال مباشرة بين الطرفين، بموجب عقود يوقعها الطرفان."),
       ("Both sides verified","التحقق من الطرفين","Every investor, buyer and business is checked before any introduction.","نتحقق من كل مستثمر ومشترٍ ومشروع قبل أي تعارف."),
       ("Strictly confidential","سرية تامة","Names stay private until both sides agree to meet.","تبقى الأسماء سرية حتى يوافق الطرفان على اللقاء."),
       ("Senior experts on every case","كبار الخبراء في كل مشروع","Experienced advisors from the first call, not junior sales staff.","مستشارون متمرسون منذ المكالمة الأولى، وليس موظفي مبيعات."),
       ("Everything in writing","كل شيء مكتوب","Scope, timeline and fees agreed in writing before any work starts.","النطاق والمدة والرسوم متفق عليها كتابةً قبل بدء أي عمل."),
       ("Any industry, any size","أي قطاع، أي حجم","From a single shop to a large group, with the right specialists for you.","من متجر واحد إلى مجموعة كبيرة، مع المتخصصين المناسبين لك.")]
why_html = "".join(f'<div>{CHECK}{t(f"wy{i}", a, b, "h3")}{t(f"wy{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(why))
steps3 = [("One free call","مكالمة مجانية واحدة","Sixty minutes with a senior advisor. We tell you honestly whether we can help.","ستون دقيقة مع أحد كبار المستشارين، نوضح لك خلالها بصراحة مدى قدرتنا على مساعدتك."),
          ("A clear plan in writing","خطة واضحة ومكتوبة","What we will do, who does it, how long it takes and what it costs.","نطاق العمل، والمسؤولون عن التنفيذ، والمدة، والتكلفة."),
          ("We stay until it’s done","نبقى معك حتى يكتمل العمل","The deal closed, the business launched, the problem fixed. Then we keep measuring.","حتى إتمام الصفقة أو إطلاق المشروع أو حل المشكلة، ثم نواصل متابعة النتائج.")]
s3 = "".join(f'<div class="s6"><div class="n">0{i+1}</div>{t(f"hw{i}", a, b, "h3")}{t(f"hw{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(steps3))
TQ = [("Daraj prepared our numbers and introduced us to three serious investors. We signed with a strategic partner within months, and they stayed with us until the last signature.", "أعدّ درج أرقامنا وعرّفنا على ثلاثة مستثمرين جادين، ووقّعنا مع شريك استراتيجي خلال أشهر، وبقي الفريق معنا حتى آخر توقيع.", "Business owner · Daraj Capital", "صاحب شركة · درج كابيتال"),
      ("What I value most is the network. I met investors I now co-invest with, and they researched a market I could never have studied alone.", "أكثر ما أقدّره هو شبكة العلاقات؛ تعرّفت على مستثمرين أستثمر معهم اليوم، ودرس الفريق سوقًا لم أكن لأدرسه وحدي.", "Investor · Investors Club", "مستثمر · نادي المستثمرين"),
      ("I used to spend my evenings on accounts. Now I get a clear report every month and spend my time on customers.", "كنت أقضي أمسياتي في الحسابات، واليوم يصلني تقرير واضح كل شهر وأتفرغ لعملائي.", "Company founder · Daraj Departments", "مؤسس شركة · درج للإدارات")]
def tq_html(p, items):
    return "".join(f'<figure>{t(f"{p}sm{i}", "Sample", "نموذج", "span", 'class="smp"')}<blockquote>{t(f"{p}{i}", "“" + a + "”", "«" + b + "»")}</blockquote><figcaption>{t(f"{p}{i}n", c, d)}</figcaption></figure>' for i, (a, b, c, d) in enumerate(items))
tq = tq_html("tq", TQ)
exec(open("/home/claude/daraj_web/articles_data.py", encoding="utf-8").read())
ARTS = [(a["slug"], a["cat"][0], a["cat"][1], a["title"][0], a["title"][1], a["desc"][0], a["desc"][1], a["filter"], a["read"][0], a["read"][1], a["img"], a["alt"][0], a["alt"][1]) for a in ARTICLES]
def cover(a, h=170):
    return f'<img src="images/{a[10]}.jpg" alt="{a[11]}" data-alt-ar="{a[12]}" loading="lazy" width="1600" height="900" style="display:block;width:100%;height:{h}px;object-fit:cover">'
def art_cards(p, n=None, items=None):
    items = items if items is not None else ARTS[:n]
    return "".join(f'<a class="icard" href="{a[0]}" data-cat="{a[7]}">{cover(a)}<div class="bd">{t(f"{p}c{i}", a[1], a[2], "span", "class=\"cat\"")}{t(f"{p}t{i}", a[3], a[4], "h3")}{t(f"{p}d{i}", a[5], a[6], "p")}{t(f"{p}m{i}", a[8], a[9], "span", "class=\"meta\"")}</div></a>' for i, a in enumerate(items))

home = f'''<section class="hero" id="top"><div class="wrap">
 <div class="split">
  <div class="a">
   {t("h_eb","Take the next step","اتخذ الخطوة التالية","div",'class="eyebrow" style="color:var(--gold)"')}
   {t("h_h1","Where capital<br>meets business.","حيث يلتقي المال<br>بالأعمال.","h1",'style="font-size:clamp(42px,6vw,72px);margin-top:14px"')}
   {t("h_lead","Step by step, we connect investors with real businesses and with each other, and help owners start, fix, grow or sell. One experienced team, open to every industry and every size.","خطوة بخطوة، نربط المستثمرين بمشاريع حقيقية وببعضهم بعضًا، ونساعد أصحاب الأعمال على البدء والإصلاح والنمو والبيع. فريق واحد من الخبراء، ومفتوح لكل القطاعات وكل الأحجام.","p",'class="lead"')}
   <div class="ctas">{t("h_c1","Book a free call","احجز مكالمة مجانية","a",'class="btn btn-gold" href="#start"')}{t("h_c2","Explore our services","اكتشف خدماتنا","a",'class="btn btn-line" href="#doors" style="color:#fff"')}</div>
   <div class="trust"><span>{CHECK}{t("h_t0","Free 60-minute call","مكالمة مجانية لمدة ٦٠ دقيقة")}</span><span>{CHECK}{t("h_t1","We never touch your money","لا نلمس أموالك أبدًا")}</span><span>{CHECK}{t("h_t2","Strictly confidential","سرية تامة")}</span></div>
  </div>
  <div class="b">{HERO_SVG}</div>
 </div>
 <div style="margin-top:56px">{t("h_q","What do you want to do?","ماذا تريد أن تفعل؟","h2",'style="font-size:28px"')}<div class="pick">{chip_html}</div></div>
</div></section>
<section class="ivory" id="doors"><div class="wrap">
 <div class="sec-head">{t("d_eb","Two doors, one team","بابان، وفريق واحد","div",'class="eyebrow"')}{t("d_h2","Choose your door.","اختر بابك.","h2")}{t("d_p","Daraj Invest is about money and ownership. Daraj Business is about fixing, growing and running what you already have.","درج للاستثمار للمال والملكية. ودرج للأعمال لإصلاح ما تملكه وتنميته وإدارته.","p")}</div>
 <div class="doors">
  {door("n","di",("Daraj Invest","درج للاستثمار"),("Raise, invest, sell or start.","التمويل والاستثمار والبيع وتأسيس المشاريع."),["capital","club","safqa","bedaya"],("Daraj Invest →","درج للاستثمار ←"),"daraj-invest.html","btn-gold")}
  {door("w","db",("Daraj Business","درج للأعمال"),("Fix, grow and run your business.","تطوير مشروعك وتنميته وإدارته باحتراف."),["consult","depts","private"],("Daraj Business →","درج للأعمال ←"),"daraj-business.html","btn-navy")}
 </div>
</div></section>
<section class="pstrip"><div class="wrap"><div>{t("ps_k","Athletes · Actors · Singers · Influencers","الرياضيون · الممثلون · المطربون · المؤثرون","span",'class="k"')}{t("ps_h","Your talent built the income. Let’s make it last.","موهبتك صنعت الدخل، فلنجعله يدوم.","h2")}{t("ps_p","Meet your private business manager: one senior team for your wealth, your deals and your businesses, in strict confidence.","تعرّف على مدير أعمالك الخاص: فريق واحد من كبار الخبراء لثروتك وصفقاتك وأعمالك، بسرية تامة.","p")}</div><div>{t("ps_b","Daraj Private Advisory →","درج للاستشارات الخاصة ←","a",'class="btn btn-gold" href="daraj-private-advisory.html"')}</div></div></section>
{band("b1", ("Not sure which door is yours?","لست متأكدًا أي باب يناسبك؟"), ("One free call is enough. We listen, then point you to the right next step.","مكالمة مجانية واحدة تكفي؛ نستمع إليك، ثم نرشدك إلى الخطوة المناسبة."))}
<section id="how"><div class="wrap">
 <div class="sec-head">{t("hw_eb","How Daraj works","كيف يعمل درج","div",'class="eyebrow"')}{t("hw_h2","Three steps. No surprises.","ثلاث خطوات. بلا مفاجآت.","h2")}</div>
 <div class="steps6" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{s3}</div>
 <div style="margin-top:28px">{t("hw_c","Start with step one","ابدأ بالخطوة الأولى","a",'class="btn btn-navy" href="#start"')}</div>
</div></section>
<section class="ivory"><div class="wrap">
 <div class="sec-head">{t("wy_eb","Why Daraj","لماذا درج","div",'class="eyebrow"')}{t("wy_h2","Built on trust, step by step.","مبني على الثقة، خطوة بخطوة.","h2")}</div>
 <div class="why">{why_html}</div>
</div></section>
<section><div class="wrap">
 <div class="sec-head">{t("tq_eb","In their words","بكلماتهم","div",'class="eyebrow"')}{t("tq_h2","What our clients say.","ماذا يقول عملاؤنا.","h2")}</div>
 <div class="tq">{tq}</div>
</div></section>
<section class="ivory" id="insights"><div class="wrap">
 <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:40px"><div class="sec-head" style="margin:0">{t("in_eb","Daraj Insights","رؤى درج","div",'class="eyebrow"')}{t("in_h2","Latest articles","أحدث المقالات","h2")}{t("in_p","Practical, honest ideas on money, deals and growth, for owners and investors.","أفكار عملية وصريحة عن المال والصفقات والنمو، لأصحاب الأعمال والمستثمرين.","p")}</div>{t("in_all","All articles →","كل المقالات ←","a",'class="btn btn-navy" href="daraj-insights.html"')}</div>
 <div class="ins">{art_cards("hm", 3)}</div>
</div></section>
<section class="dark" id="majlis" style="background:var(--navy2);color:#fff"><div class="wrap split">
 <div class="a">{t("mj_eb","Daraj Majlis","مجلس درج","div",'class="eyebrow"')}{t("mj_h2","A circle of investors and owners.","دائرة تجمع المستثمرين وأصحاب الأعمال.","h2",'style="margin:14px 0 18px"')}{t("mj_p","Small, private sessions where investors meet investors and business owners, share real cases and build trust before any deal. Membership is by invitation after a first call.","جلسات صغيرة وخاصة يلتقي فيها المستثمرون بمستثمرين آخرين وبأصحاب الأعمال، يتبادلون حالات حقيقية ويبنون الثقة قبل أي صفقة. العضوية بدعوة بعد المكالمة الأولى.","p",'style="color:#C9D2DE;font-size:18px;max-width:600px"')}</div>
 <div class="b"><div class="majcard">{t("mj_k","NEXT SESSION","الجلسة القادمة","span",'style="color:var(--gold);font-weight:700;font-size:13px"')}{t("mj_t","[Session topic]","[موضوع الجلسة]","b",'style="font-size:22px"')}{t("mj_d","[Date] · [City or online]","[التاريخ] · [المدينة أو عبر الإنترنت]","span",'style="color:#C9D2DE"')}<div>{t("mj_c","Request an invitation","اطلب دعوة","a",'class="btn btn-gold" href="#start"')}</div></div></div>
</div></section>
<section class="ivory"><div class="wrap faq">
 <div class="sec-head">{t("faq_eyebrow","Questions people ask","أسئلة شائعة","div",'class="eyebrow"')}{t("faq_h2","Frequently asked questions","الأسئلة الشائعة","h2")}</div>
 {"".join(f'<details>{t(f"hq{i}", a, b, "summary")}{t(f"ha{i}", c, d, "p")}</details>' for i, (a, b, c, d) in enumerate([
   ("Is the first call really free?","هل المكالمة الأولى مجانية فعلًا؟","Yes. Sixty minutes, no cost and no obligation. If we can’t help, we will say so.","نعم. ستون دقيقة بلا تكلفة وبلا أي التزام. وإن لم نستطع المساعدة، سنقول ذلك بصراحة."),
   ("Do you hold investors’ money?","هل تحتفظون بأموال المستثمرين؟","Never. Money moves directly between investor and business, under contracts both sides sign.","أبدًا. الأموال تنتقل مباشرة بين المستثمر والمشروع، بموجب عقود يوقّعها الطرفان."),
   ("Will my information stay confidential?","هل تبقى معلوماتي سرية؟","Yes. We work under confidentiality agreements, and names stay hidden until both sides agree to meet.","نعم. نعمل باتفاقيات سرية، وتبقى الأسماء مخفية حتى يوافق الطرفان على اللقاء."),
   ("Can you find investment opportunities in a specific country?","هل يمكنكم إيجاد فرص استثمار في دولة محددة؟","Yes. Tell us the country, sector and ticket size, and our Investors Club team researches the market and searches for you.","نعم. أخبرنا بالدولة والقطاع وحجم الاستثمار، وسيتولى فريق نادي المستثمرين دراسة السوق والبحث عن الفرص المناسبة لك."),
   ("Who is Daraj for?","لمن يقدم درج خدماته؟","Investors, owners, sellers and people ready to start, in any industry and at any size. The free call tells us which door fits you.","للمستثمرين وأصحاب الأعمال والبائعين ومن يستعد لبدء مشروعه، في أي قطاع وبأي حجم. والمكالمة المجانية تحدد الباب المناسب لك.")]))}
</div></section>
{contact_form("hm", ("Take the next step: one free call.","اتخذ الخطوة التالية: مكالمة مجانية واحدة."), ("Tell us where you are. A senior advisor will show you the next step.","حدّثنا عن وضعك الحالي، وسيوضح لك أحد كبار مستشارينا الخطوة التالية."), STD_STEPS, basic_fields("hm"), ("Book my free call →","احجز مكالمتي المجانية ←"), THX)}
'''
build("index.html", "", "Daraj — Take the next step | Where capital meets business", "Daraj connects investors with real businesses and with each other, and helps owners start, fix, grow or sell. Start with a free call.", home)

# ===== DOOR PAGES =====
def door_page(fname, key, cur, name, tag, lead, svcs, details, guide):
    AR.clear()
    cards = ""
    for i, k in enumerate(svcs):
        href, en, ar, sl, sla = SVC[k]
        d = details[k]
        bl = "".join(f'<li style="margin:6px 0">{t(f"{key}xb{i}{j}", a, b)}</li>' for j, (a, b) in enumerate(d[2]))
        cards += f'''<div class="door {"n" if i % 2 == 0 else "w"}" style="gap:14px">
  {t(f"{key}xk{i}", sl, sla, "div", 'class="eyebrow"' + (' style="color:var(--gold)"' if i % 2 == 0 else ""))}
  {t(f"{key}xh{i}", en, ar, "h3")}
  {t(f"{key}xp{i}", d[0], d[1], "p", 'class="sub" style="font-size:17px"')}
  <ul style="margin:0;padding-inline-start:20px">{bl}</ul>
  <div>{t(f"{key}xc{i}", en + " →", ar + " ←", "a", f'class="btn {"btn-gold" if i % 2 == 0 else "btn-navy"}" href="{href}"')}</div>
</div>'''
    gr = "".join(f'<a class="rel" href="{SVC[k][0]}">{t(f"{key}xg{i}", a, b, "h3")}{t(f"{key}xgp{i}", SVC[k][1] + " →", SVC[k][2] + " ←", "p")}</a>' for i, (a, b, k) in enumerate(guide))
    body = f'''<div class="crumb"><div class="wrap"><a href="index.html" data-i18n="nav_home">Home</a> / <span style="color:#fff" data-i18n="{key}cr">{name[0]}</span></div></div>
<section class="hero" id="top"><div class="wrap split">
 <div class="a">{t(key+"eb", *tag, "div", 'class="eyebrow" style="color:var(--gold)"')}{t(key+"h1", *name, "h1", 'style="font-size:clamp(42px,6vw,68px);margin-top:14px"')}{t(key+"ld", *lead, "p", 'class="lead"')}
  <div class="ctas">{t(key+"c1","Book a free call","احجز مكالمة مجانية","a",'class="btn btn-gold" href="#start"')}{t(key+"c2","See the services","تعرّف على الخدمات","a",'class="btn btn-line" href="#services" style="color:#fff"')}</div></div>
 <div class="b">{HERO_SVG}</div>
</div></section>
<section class="ivory" id="services"><div class="wrap"><div class="doors">{cards}</div></div></section>
<section><div class="wrap"><div class="sec-head">{t(key+"geb","Which one is for me?","أيها يناسبني؟","div",'class="eyebrow"')}{t(key+"gh2","Start from what you want to do.","ابدأ مما تريد أن تفعله.","h2")}</div><div class="related">{gr}</div></div></section>
{tq_section(key+"tq", [SVC_TQ[k][0] for k in (svcs if len(svcs) > 2 else svcs + ["consult"])][:3])}
{band(key, ("Still not sure? One call answers it.","لست متأكدًا بعد؟ مكالمة واحدة تكفي."), ("A senior advisor will tell you which service fits, and what the next step is.","سيحدد لك أحد كبار مستشارينا الخدمة المناسبة والخطوة التالية."))}
{contact_form(key, ("Book your free call.","احجز مكالمتك المجانية."), ("Tell us the basics and a senior advisor will prepare for your call.","زوّدنا بالمعلومات الأساسية، وسيستعد أحد كبار مستشارينا لمكالمتك."), STD_STEPS, basic_fields(key), ("Book my free call →","احجز مكالمتي المجانية ←"), THX)}'''
    AR["nav_home"] = "الرئيسية"; AR[key+"cr"] = name[1]
    build(fname, cur, f"{name[0]} — Daraj", lead[0], body)

AR.clear()
door_page("daraj-invest.html", "iv", "div_invest", ("Daraj Invest", "درج للاستثمار"), ("Money and ownership", "المال والملكية"),
  ("Raise capital, invest and connect with investors, sell your business, or start a new one, with one team beside you at every step.", "موّل مشروعك، أو استثمر وتواصل مع المستثمرين، أو بِع مشروعك، أو ابدأ مشروعًا جديدًا، مع فريق واحد بجانبك في كل خطوة."),
  ["capital", "club", "safqa", "bedaya"],
  {"capital": ("For business owners who want investment or a strategic partner.", "لأصحاب الأعمال الذين يريدون استثمارًا أو شريكًا استراتيجيًا.", [("Valuation range and investor-ready numbers", "نطاق تقييم وأرقام جاهزة للمستثمرين"), ("Investors and strategic partners matched to you", "مستثمرون وشركاء استراتيجيون مناسبون لك"), ("Support until the deal is signed", "دعم حتى توقيع الصفقة")]),
   "club": ("For investors who want reviewed opportunities and a real network.", "للمستثمرين الذين يريدون فرصًا تمت مراجعتها وشبكة علاقات حقيقية.", [("Opportunities checked before you see them", "فرص نتحقق منها قبل أن تراها"), ("Investors meet investors and co-invest", "المستثمرون يلتقون ويستثمرون معًا"), ("Search and research in any country", "بحث ودراسة في أي دولة")]),
   "safqa": ("For owners ready to sell, confidentially and at the right price.", "لأصحاب الأعمال المستعدين للبيع، بسرية وبالسعر المناسب.", [("Asking-price guidance and a sale file", "إرشاد للسعر المطلوب وملف بيع احترافي"), ("Anonymous listing, verified buyers only", "عرض بدون اسم، ومشترون موثقون فقط"), ("Free during our Founding Period", "مجانًا خلال فترة التأسيس")]),
   "bedaya": ("For people with capital who want their own business.", "لمن يملك رأس المال ويريد مشروعه الخاص.", [("Ideas researched for your money and time", "أفكار مدروسة تناسب مالك ووقتك"), ("Plan, build and launch with us", "خطط وابنِ وأطلق مشروعك معنا"), ("Keep your job if you want", "احتفظ بوظيفتك إن أردت")])},
  [("I need investment or a partner", "أحتاج استثمارًا أو شريكًا", "capital"), ("I want to invest or meet investors", "أريد أن أستثمر أو ألتقي بمستثمرين", "club"), ("I want to sell my business", "أريد بيع مشروعي", "safqa"), ("I want to start a business", "أريد بدء مشروع", "bedaya")])
door_page("daraj-business.html", "bz", "div_bs", ("Daraj Business", "درج للأعمال"), ("Fix, grow and run", "إصلاح ونمو وإدارة"),
  ("Solve the real problems in your business with consulting, or let our team run your departments every month, for any industry and any size.", "حُلّ المشكلات الحقيقية في مشروعك عبر الاستشارات، أو دع فريقنا يدير إداراتك كل شهر، لأي قطاع وأي حجم."),
  ["consult", "depts", "private"],
  {"private": ("One-to-one senior advice for owners and executives, and a private business manager for athletes, actors, singers and influencers.", "استشارات فردية من كبار الخبراء لأصحاب الأعمال والتنفيذيين، ومدير أعمال خاص للرياضيين والممثلين والمطربين والمؤثرين.", [("A senior advisor in your corner", "مستشار من كبار الخبراء إلى جانبك"), ("Every deal checked before you sign", "دراسة كل صفقة قبل توقيعك"), ("Strictly confidential, limited clients", "بسرية تامة ولعدد محدود من العملاء")]),
   "consult": ("We find the real cause, design the solution and measure the results.", "نجد السبب الحقيقي، ونصمم الحل، ونقيس النتائج.", [("Free one-hour Business X-Ray", "فحص أعمال مجاني لمدة ساعة"), ("Strategy, operations, finance, people and AI", "الاستراتيجية والعمليات والمالية والأفراد والذكاء الاصطناعي"), ("Follow-up at 30, 60 and 90 days", "متابعة بعد ٣٠ و٦٠ و٩٠ يومًا")]),
   "depts": ("Complete departments run for you, for one monthly fee based on your size.", "إدارات كاملة نديرها لك، برسوم شهرية واحدة حسب حجمك.", [("13 departments, from finance to AI", "١٣ إدارة، من المالية إلى الذكاء الاصطناعي"), ("Senior leaders as a service", "قيادات عليا كخدمة"), ("Reports and review calls every month", "تقارير ومكالمات مراجعة شهرية")])},
  [("Something is not working and I want it fixed", "هناك شيء لا يعمل وأريد إصلاحه", "consult"), ("I need a team to run my departments", "أحتاج فريقًا يدير إداراتي", "depts"), ("I want a private business manager or a senior advisor", "أريد مدير أعمال خاصًا أو مستشارًا من كبار الخبراء", "private")])

# ===== PRIVATE ADVISORY =====
AR.clear()
aud = [("A","Athletes and football players","الرياضيون ولاعبو كرة القدم","Contracts and bonuses for a few peak years, and a life that continues long after.","عقود ومكافآت في سنوات ذروة محدودة، وحياة تستمر بعدها طويلًا."),
       ("B","Actors","الممثلون","Income project by project, with long gaps between them.","دخل يأتي من عمل لآخر، مع فترات انقطاع طويلة بينها."),
       ("C","Singers and musicians","المطربون والموسيقيون","Concerts, tours, royalties and rights, with income from many sources and many countries.","حفلات وجولات وعائدات وحقوق، ودخل من مصادر ودول متعددة."),
       ("D","Influencers and content creators","المؤثرون وصنّاع المحتوى","Brand deals and platform income that can change overnight with an algorithm.","صفقات مع العلامات التجارية ودخل من المنصات قد يتغير بين ليلة وضحاها."),
       ("E","TV presenters and public figures","مقدمو البرامج والشخصيات العامة","A public name that attracts offers, and a reputation that must be protected.","اسم معروف يجذب العروض، وسمعة يجب حمايتها."),
       ("F","High-earning professionals","أصحاب الدخل المرتفع","Anyone whose income grew faster than their time to manage it.","كل من نما دخله أسرع من الوقت المتاح لإدارته.")]
ICONS = ["⚽","🎬","🎤","📱","📺","★"]
aud_html = "".join(f'<div><div class="ic">{ICONS[i]}</div>{t(f"au{i}", a, b, "h3")}{t(f"au{i}p", c, d, "p")}</div>' for i, (_, a, b, c, d) in enumerate(aud))
real = [("A short peak, a long life","ذروة قصيرة وحياة طويلة","The years you earn the most may be few; the plan must last decades.","قد تكون سنوات الدخل الأعلى قليلة، والخطة يجب أن تدوم لعقود."),
        ("Irregular income","دخل غير منتظم","Contracts, tours, campaigns and seasons; some months huge, others nothing.","عقود وجولات وحملات ومواسم؛ أشهر بدخل كبير وأخرى بلا دخل."),
        ("Everyone has a deal for you","الجميع لديه صفقة لك","Friends, relatives and strangers pitch restaurants, brands and “guaranteed” investments.","أصدقاء وأقارب وغرباء يعرضون مطاعم وعلامات تجارية واستثمارات «مضمونة»."),
        ("Your name is your biggest asset","اسمك هو أكبر أصولك","One bad partnership can cost money and reputation.","شراكة واحدة خاطئة قد تكلفك المال والسمعة."),
        ("No time","لا وقت لديك","Training, filming, touring and creating leave no time to follow your money.","التدريب والتصوير والجولات وصناعة المحتوى لا تترك وقتًا لمتابعة أموالك.")]
real_html = "".join(f'<div>{t(f"re{i}", a, b, "h3")}{t(f"re{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(real))
svc = [("Your personal wealth plan","خطة ثروتك الشخصية","How much to spend, save, invest and protect, built around your career stage.","كم تنفق وتدّخر وتستثمر وتحمي، وفق مرحلة مسيرتك المهنية."),
       ("We check every deal before you sign","ندرس كل صفقة قبل توقيعك","Every business, partnership or investment pitched to you comes to us first, and we tell you the truth.","كل مشروع أو شراكة أو استثمار يُعرض عليك يمرّ علينا أولًا، ونصارحك بالحقيقة."),
       ("Build your own brand or business","ابنِ علامتك أو مشروعك الخاص","Turn your name into a company you own: a product line, a restaurant, an academy or a studio, set up properly.","حوّل اسمك إلى شركة تملكها، سواء كانت خط منتجات أو مطعمًا أو أكاديمية أو استوديو، بتأسيس سليم."),
       ("Invest for life after the peak","استثمر لما بعد الذروة","Reviewed opportunities and serious co-investors through the Daraj Investors Club.","فرص تمت مراجعتها ومستثمرون جادون من خلال نادي المستثمرين في درج."),
       ("Oversee the businesses you already own","الإشراف على أعمالك القائمة","Monthly reports, performance reviews and accountability for the people running them.","تقارير شهرية ومراجعة للأداء ومساءلة للقائمين عليها."),
       ("One point of contact","جهة تواصل واحدة","We work alongside your agent or talent manager, lawyer, accountant and bank, so everything is coordinated.","نعمل جنبًا إلى جنب مع وكيلك أو مدير أعمالك الفني ومحاميك ومحاسبك والبنك، لتكون كل الأمور منسّقة.")]
svc_html = "".join(f'<div>{CHECK}{t(f"sv{i}", a, b, "h3")}{t(f"sv{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(svc))
own = [("Monthly strategy sessions","جلسات استراتيجية شهرية"),("Direct line to your advisor","تواصل مباشر مع مستشارك"),("A second opinion on major decisions and deals","رأي ثانٍ في القرارات والصفقات الكبرى"),("Board-level support for your management team","دعم على مستوى مجلس الإدارة لفريقك الإداري")]
own_html = "".join(f'<div>{CHECK}{t(f"ow{i}", a, b, "h3")}</div>' for i, (a, b) in enumerate(own))
hw = [("Private consultation","استشارة خاصة","Confidential, anywhere in the world.","بسرية تامة، ومن أي مكان في العالم."),
      ("Your plan","خطتك","A clear written plan within weeks.","خطة مكتوبة وواضحة خلال أسابيع."),
      ("We put it to work","نبدأ التنفيذ","Deals, businesses and investments, as agreed.","الصفقات والأعمال والاستثمارات، وفق ما اتفقنا عليه."),
      ("Regular reporting","تقارير منتظمة","Monthly updates, around your schedule, wherever you are.","تحديثات شهرية تناسب جدولك، أينما كنت.")]
hw_html = "".join(f'<div class="s6"><div class="n">0{i+1}</div>{t(f"pw{i}", a, b, "h3")}{t(f"pw{i}p", c, d, "p")}</div>' for i, (a, b, c, d) in enumerate(hw))
PTQ = [("I had three ‘once in a lifetime’ offers in one season. Daraj checked them all. Two would have cost me a lot. The third is now a business I own.", "عُرضت عليّ ثلاث فرص «لا تتكرر» في موسم واحد، فدرسها درج كلها؛ اثنتان كانتا ستكلفانني الكثير، والثالثة أصبحت اليوم مشروعًا أملكه.", "Professional footballer · Private Advisory", "لاعب كرة قدم محترف · الاستشارات الخاصة"),
       ("My income comes from tours, rights and campaigns in different countries. For the first time I have one plan and one team that sees everything.", "يأتي دخلي من الجولات والحقوق والحملات في دول مختلفة، ولأول مرة أصبحت لديّ خطة واحدة وفريق واحد يرى الصورة كاملة.", "Singer · Private Advisory", "مطرب · الاستشارات الخاصة"),
       ("They helped me turn my audience into a brand I actually own, set up properly, with numbers I receive every month.", "ساعدوني على تحويل جمهوري إلى علامة تجارية أملكها فعلًا، بتأسيس سليم وأرقام تصلني كل شهر.", "Content creator · Private Advisory", "صانعة محتوى · الاستشارات الخاصة")]
pfaq = [("I already have an agent. Do I need you?","لدي وكيل بالفعل، فهل أحتاج إليكم؟","Yes, for a different job. Your agent grows your career; we grow and protect what you earn from it.","نعم، ولمهمة مختلفة؛ فوكيلك ينمّي مسيرتك، ونحن ننمّي ما تكسبه منها ونحميه."),
        ("Do you invest my money for me?","هل تستثمرون أموالي نيابةً عني؟","No. Your money stays in your accounts and you approve every decision. We plan, check and oversee, with licensed partners where required.","لا. تبقى أموالك في حساباتك وتعتمد أنت كل قرار، ودورنا التخطيط والدراسة والإشراف، مع شركاء مرخّصين عند الحاجة."),
        ("Will anyone know I work with you?","هل سيعرف أحد أنني أتعامل معكم؟","Only if you want them to. Confidentiality is part of every agreement, and we sign an NDA from day one.","فقط إن رغبت في ذلك؛ فالسرية جزء من كل اتفاق، ونوقّع اتفاقية سرية منذ اليوم الأول."),
        ("I travel all the time. Does that work?","أنا كثير السفر، فهل يناسبني ذلك؟","Yes. We work by video, phone and in person, around your schedule, wherever you are.","نعم. نعمل عبر الفيديو والهاتف واللقاءات المباشرة، وبما يناسب جدولك أينما كنت."),
        ("Is this only for celebrities?","هل الخدمة للمشاهير فقط؟","No. It is for anyone with significant income or wealth and little time to manage it, including business owners and executives.","لا. إنها لكل من لديه دخل أو ثروة كبيرة ووقت محدود لإدارتها، بمن فيهم أصحاب الأعمال والتنفيذيون.")]
pf = [field("pvfn","Full name","الاسم الكامل"), field("pvfw","WhatsApp number","رقم واتساب","tel"), field("pvfe","Email","البريد الإلكتروني","email"), field("pvfc","Country of residence","دولة الإقامة"),
      field("pvfi","I am","أنا","select", items=[("Choose","اختر"),("Business owner","صاحب أعمال"),("Executive","مسؤول تنفيذي"),("Athlete / football player","رياضي / لاعب كرة قدم"),("Actor","ممثل"),("Singer / musician","مطرب / موسيقي"),("Influencer / content creator","مؤثر / صانع محتوى"),("TV presenter / public figure","مقدم برامج / شخصية عامة"),("Other","أخرى")]),
      field("pvfm","Approximate wealth or annual income to plan for (USD)","الثروة أو الدخل السنوي التقريبي المطلوب التخطيط له (بالدولار الأمريكي)","select", items=[("Choose","اختر"),("Less than $250,000","أقل من ٢٥٠ ألف دولار"),("$250,000 – $1 million","من ٢٥٠ ألفًا إلى مليون دولار"),("$1 – 5 million","من مليون إلى ٥ ملايين دولار"),("More than $5 million","أكثر من ٥ ملايين دولار"),("Prefer to discuss on the call","أفضّل مناقشته في المكالمة")]),
      field("pvfn1","What do you need first?","ما أول ما تحتاج إليه؟","select", items=[("Choose","اختر"),("A wealth plan","خطة للثروة"),("Checking a deal","دراسة صفقة"),("Building my brand or business","بناء علامتي أو مشروعي"),("Overseeing my businesses","الإشراف على أعمالي"),("Investing","الاستثمار"),("Strategic advice for my company","استشارة استراتيجية لشركتي")]),
      field("pvfa","Do you have an agent or manager?","هل لديك وكيل أو مدير أعمال؟","select", items=[("Choose","اختر"),("Yes","نعم"),("No","لا")]),
      t("pvnote","Every request is reviewed personally and handled in strict confidence.","تُراجع كل الطلبات شخصيًا وتُعامل بسرية تامة.","p",'class="full" style="margin:-4px 0 0;font-size:13px;color:var(--muted)"')]
PSTEPS = [("Tell us the basics","أخبرنا بالأساسيات","Two minutes, in strict confidence.","دقيقتان فقط، وبسرية تامة."),("A private consultation","استشارة خاصة","With a senior advisor, by video, phone or in person.","مع أحد كبار المستشارين، عبر الفيديو أو الهاتف أو لقاءً مباشرًا."),("Your plan in writing","خطتك مكتوبة","Clear, honest and built around you.","واضحة وصريحة ومصممة حولك.")]
pbody = f'''<div class="crumb"><div class="wrap"><a href="index.html" data-i18n="nav_home">Home</a> / <a href="daraj-business.html" data-i18n="pv_cb">Daraj Business</a> / <span style="color:#fff" data-i18n="pv_cr">Private Advisory</span></div></div>
<section class="hero" id="top"><div class="wrap split">
 <div class="a">{t("pv_eb","Daraj Private Advisory · Confidential, limited clients","درج للاستشارات الخاصة · بسرية تامة ولعدد محدود من العملاء","div",'class="eyebrow" style="color:var(--gold)"')}
  {t("pv_h1","A senior advisor in your corner, for your business and your wealth.","مستشار من كبار الخبراء إلى جانبك، لأعمالك وثروتك.","h1",'style="font-size:clamp(36px,4.6vw,56px);margin-top:14px"')}
  {t("pv_ld","One-to-one advisory for business owners and executives, and a dedicated private business manager for public figures and high earners.","استشارات فردية لأصحاب الأعمال والتنفيذيين، ومدير أعمال خاص للشخصيات العامة وأصحاب الدخل المرتفع.","p",'class="lead"')}
  <div class="ctas">{t("pv_c1","Request a private consultation","اطلب استشارة خاصة","a",'class="btn btn-gold" href="#start"')}{t("pv_c2","Chat on WhatsApp","تواصل عبر واتساب","a",'class="btn btn-line" href="#start" style="color:#fff"')}</div></div>
 <div class="b"><div class="heroaud">{t("pv_hk","Every client receives","ما يحصل عليه كل عميل","b",'style="color:var(--gold);font-size:13px;letter-spacing:.08em;text-transform:uppercase"')}
  <ul class="hlist">{"".join(f'<li>{CHECK}<div>{t(f"pv_hl{i}", a, b, "strong")}{t(f"pv_hl{i}p", c, d, "span")}</div></li>' for i, (a, b, c, d) in enumerate([
   ("A dedicated senior advisor","مستشار مخصص من كبار الخبراء","One person who knows your situation, with direct access.","شخص واحد يعرف وضعك، مع تواصل مباشر."),
   ("An independent second opinion","رأي ثانٍ مستقل","Every major decision and deal reviewed before you commit.","مراجعة كل قرار وصفقة كبرى قبل أن تلتزم."),
   ("Complete discretion","سرية تامة","An NDA from day one. Your name is never shared.","اتفاقية سرية منذ اليوم الأول، ولا نشارك اسمك أبدًا."),
   ("Your money stays yours","أموالك تبقى لك","Funds remain in your own accounts; every decision is yours.","تبقى أموالك في حساباتك، وكل قرار بيدك.")]))}</ul>
  {t("pv_hn","By consultation only · Limited clients","بموعد مسبق فقط · لعدد محدود من العملاء","p",'style="margin:18px 0 0;color:#9FB0C6;font-size:13px"')}
 </div></div>
</div></section>
<section class="ivory"><div class="wrap">
 <div class="sec-head">{t("pa_eb","Two paths, one standard","مساران، ومعيار واحد","div",'class="eyebrow"')}{t("pa_h2","Choose the path that fits you.","اختر المسار الذي يناسبك.","h2")}</div>
 <div class="paths">
  <a class="pathc" href="#owners">{t("pa1k","Path 1","المسار الأول","span",'class="k"')}{t("pa1h","For business owners and executives","لأصحاب الأعمال والتنفيذيين","h3")}{t("pa1p","A senior advisor who knows your business, for strategy, growth and difficult decisions.","مستشار من كبار الخبراء يعرف أعمالك، للاستراتيجية والنمو والقرارات الصعبة.","p")}{t("pa1b","Explore →","اكتشف المزيد ←","b")}</a>
  <a class="pathc g" href="#talent">{t("pa2k","Path 2","المسار الثاني","span",'class="k"')}{t("pa2h","Your private business manager","مدير أعمالك الخاص","h3")}{t("pa2p","For athletes, football players, actors, singers, musicians, influencers and content creators.","للرياضيين ولاعبي كرة القدم والممثلين والمطربين والموسيقيين والمؤثرين وصنّاع المحتوى.","p")}{t("pa2b","Explore →","اكتشف المزيد ←","b")}</a>
 </div>
</div></section>
<section id="owners"><div class="wrap split">
 <div class="a">{t("ow_eb","Path 1 · Business owners and executives","المسار الأول · أصحاب الأعمال والتنفيذيون","div",'class="eyebrow"')}{t("ow_h2","A senior advisor who knows your business.","مستشار من كبار الخبراء يعرف أعمالك.","h2",'style="margin:12px 0 14px"')}{t("ow_p","Big decisions are lonely. Work one-to-one with a senior advisor on strategy, growth, partnerships and difficult decisions, with direct access whenever you need it.","القرارات الكبيرة تحتاج إلى من تستشيره. اعمل بشكل فردي مع أحد كبار المستشارين في الاستراتيجية والنمو والشراكات والقرارات الصعبة، مع تواصل مباشر متى احتجت إليه.","p",'style="font-size:18px;color:var(--muted)"')}<div style="margin-top:22px">{t("ow_c","Request a private consultation","اطلب استشارة خاصة","a",'class="btn btn-navy" href="#start"')}</div></div>
 <div class="b"><div class="why" style="grid-template-columns:1fr">{own_html}</div></div>
</div></section>
<section class="dark" id="talent" style="background:var(--navy);color:#fff"><div class="wrap">
 <div class="sec-head">{t("tl_eb","Path 2 · For athletes, artists and creators","المسار الثاني · للرياضيين والفنانين وصنّاع المحتوى","div",'class="eyebrow" style="color:var(--gold)"')}{t("tl_h2","You focus on your talent. We take care of your business.","ركّز على موهبتك، ونحن نهتم بأعمالك.","h2",'style="color:#fff"')}{t("tl_p","Whether you play on the pitch, perform on stage, act on screen or build an audience online, your income works differently from anyone else’s. We understand that, and we built this service around it.","سواء كنت تلعب في الملعب، أو تغني على المسرح، أو تمثّل على الشاشة، أو تبني جمهورك عبر الإنترنت، فدخلك يختلف عن دخل أي شخص آخر. نحن نفهم ذلك، وصمّمنا هذه الخدمة على هذا الأساس.","p",'style="color:#C9D2DE"')}</div>
 <div class="sec-head" style="margin-top:20px">{t("rl_h","Fame and income bring problems most advisors never see.","الشهرة والدخل المرتفع يجلبان تحديات لا يراها معظم المستشارين.","h3",'style="color:#fff;font-size:22px"')}</div>
 <div class="reality">{real_html}</div>
</div></section>
<section class="ivory"><div class="wrap">
 <div class="sec-head">{t("au_eb","Path 2 · Who it is for","المسار الثاني · لمن صُمّم","div",'class="eyebrow"')}{t("au_h2","Built for people whose income works differently.","مصممة لمن يختلف دخلهم عن غيرهم.","h2")}</div>
 <div class="aud">{aud_html}</div>
</div></section>
<section><div class="wrap">
 <div class="sec-head">{t("sv_eb","What your private business manager does","ماذا يفعل مدير أعمالك الخاص","div",'class="eyebrow"')}{t("sv_h2","One team for your wealth, your deals and your businesses.","فريق واحد لثروتك وصفقاتك وأعمالك.","h2")}</div>
 <div class="why">{svc_html}</div>
 <div class="agent">{t("ag_p","Already have an agent or manager? Perfect. They handle your career and contracts. We handle what you build with what you earn.","هل لديك وكيل أو مدير أعمال فني؟ ممتاز. هو يتولى مسيرتك وعقودك، ونحن نتولى ما تبنيه بما تكسبه.","p")}{t("ag_c","Request a private consultation →","اطلب استشارة خاصة ←","a",'class="btn btn-navy" href="#start"')}</div>
</div></section>
<section class="ivory"><div class="wrap"><div class="trustbox">
 <div style="flex:1 1 420px">{t("tr_h","Your money stays yours. Your privacy stays protected.","أموالك تبقى لك، وخصوصيتك محمية.","h2")}{t("tr_p","Daraj never holds or moves client money; your funds stay in your own accounts. Every decision is yours. Your name is never shared without your permission, and we sign an NDA from day one.","لا يحتفظ درج بأموال العملاء ولا يحرّكها، فأموالك تبقى في حساباتك وكل قرار بيدك. لا نشارك اسمك دون إذنك، ونوقّع اتفاقية سرية منذ اليوم الأول.","p")}</div>
 <div>{t("tr_c","Request a private consultation","اطلب استشارة خاصة","a",'class="btn btn-gold" href="#start"')}</div>
</div></div></section>
<section><div class="wrap">
 <div class="sec-head">{t("pw_eb","How it works","كيف نعمل","div",'class="eyebrow"')}{t("pw_h2","Four steps, around your schedule.","أربع خطوات، بما يناسب جدولك.","h2")}</div>
 <div class="steps6" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{hw_html}</div>
</div></section>
<section class="ivory"><div class="wrap">
 <div class="sec-head">{t("pq_eb","In their words","بكلماتهم","div",'class="eyebrow"')}{t("pq_h2","What our clients say.","ماذا يقول عملاؤنا.","h2")}</div>
 <div class="tq">{tq_html("pq", PTQ)}</div>
</div></section>
<section><div class="wrap faq">
 <div class="sec-head">{t("pf_eb","Questions people ask","أسئلة شائعة","div",'class="eyebrow"')}{t("pf_h2","Frequently asked questions","الأسئلة الشائعة","h2")}</div>
 {"".join(f'<details>{t(f"pfq{i}", a, b, "summary")}{t(f"pfa{i}", c, d, "p")}</details>' for i, (a, b, c, d) in enumerate(pfaq))}
</div></section>
{band("pv", ("Your talent built the income. Let’s make it last.","موهبتك صنعت الدخل، فلنجعله يدوم."), ("A confidential conversation with a senior advisor, wherever you are.","محادثة سرية مع أحد كبار المستشارين، أينما كنت."))}
{contact_form("pv", ("Request a private consultation.","اطلب استشارة خاصة."), ("Tell us a little about yourself. A senior advisor will prepare for a confidential conversation.","حدّثنا قليلًا عن نفسك، وسيستعد أحد كبار المستشارين لمحادثة سرية معك."), PSTEPS, pf, ("Request my private consultation →","اطلب استشارتي الخاصة ←"), THX)}'''
AR["nav_home"] = "الرئيسية"; AR["pv_cb"] = "درج للأعمال"; AR["pv_cr"] = "الاستشارات الخاصة"
pbody = pbody.replace('data-i18n="pvf_h">Book your free call<', 'data-i18n="pvf_h">Request a private consultation<'); AR["pvf_h"] = "اطلب استشارة خاصة"; AR["pvcta_eb"] = "بسرية تامة · بدون أي التزام"
pbody = pbody.replace('data-i18n="pvcta_eb">Free · no obligation<', 'data-i18n="pvcta_eb">Confidential · no obligation<')
build("daraj-private-advisory.html", "div_bs", "Daraj Private Advisory — Private business manager for athletes, artists and creators", "One-to-one senior advisory for business owners, and a private business manager for athletes, football players, actors, singers and influencers. Strictly confidential.", pbody)

# ===== INSIGHTS =====
AR.clear()
pills = "".join(t(f"pl{i}", a, b, "button", f'type="button" data-f="{k}"' + (' class="on"' if i == 0 else "")) for i, (a, b, k) in enumerate([("All","الكل","all"),("For owners","لأصحاب الأعمال","owners"),("For investors","للمستثمرين","investors"),("For sellers","للبائعين","sellers"),("For founders","للمؤسسين","founders"),("AI & automation","الذكاء الاصطناعي","ai")]))
ins = f'''<div class="crumb"><div class="wrap"><a href="index.html" data-i18n="nav_home">Home</a> / <span style="color:#fff" data-i18n="nav_ins">Articles</span></div></div>
<section class="hero" id="top"><div class="wrap split">
 <div class="a">{t("ih_eb","Daraj Insights","رؤى درج","div",'class="eyebrow" style="color:var(--gold)"')}{t("ih_h1","Practical ideas for money and business.","أفكار عملية للمال والأعمال.","h1",'style="font-size:clamp(40px,5.6vw,64px);margin-top:14px"')}{t("ih_ld","Short, honest articles on growth, cash, deals and AI, written for owners and investors, not for consultants.","مقالات قصيرة وصريحة عن النمو والسيولة والصفقات والذكاء الاصطناعي، مكتوبة لأصحاب الأعمال والمستثمرين، لا للمستشارين.","p",'class="lead"')}</div>
 <div class="b"><a class="icard" href="{ARTS[0][0]}" style="background:var(--navy2);border-color:#2A3D5C;color:#fff"><div class="bd">{t("if_k","Featured · For owners","مقال مميز · لأصحاب الأعمال","span",'class="cat" style="color:var(--gold)"')}{t("if_t",ARTS[0][3],ARTS[0][4],"h3",'style="font-size:26px"')}{t("if_d",ARTS[0][5],ARTS[0][6],"p",'style="color:#C9D2DE"')}{t("if_r","Read article →","اقرأ المقال ←","b",'style="color:var(--gold)"')}</div></a></div>
</div></section>
<section class="ivory"><div class="wrap"><div class="pills" id="pills">{pills}</div><div class="ins" id="grid">{art_cards("ig", len(ARTS))}</div></div></section>
<section><div class="wrap" style="max-width:760px;text-align:center">{t("nl_h","One useful idea, every two weeks.","فكرة مفيدة واحدة كل أسبوعين.","h2")}{t("nl_p","Join the Daraj newsletter. No spam, no selling, unsubscribe any time.","اشترك في النشرة البريدية لدرج. لا رسائل مزعجة، ويمكنك إلغاء الاشتراك في أي وقت.","p",'style="color:var(--muted);font-size:17px"')}
 <form style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:18px" onsubmit="event.preventDefault()"><label style="flex:1 1 300px;text-align:start;font-weight:600;font-size:14px">{t("nl_l","Email address","البريد الإلكتروني")}<input type="email" required style="display:block;width:100%;box-sizing:border-box;height:48px;margin-top:6px;padding:0 14px;border:1px solid #C9C1B1;border-radius:10px;font:inherit"></label>{t("nl_b","Subscribe","اشترك","button",'type="submit" class="btn btn-navy" style="align-self:flex-end"')}</form></div></section>
{band("ib", ("Have a question about your business?","هل لديك استفسار حول مشروعك؟"), ("Discuss it in a free call with one of our senior advisors.","ناقشه في مكالمة مجانية مع أحد كبار مستشارينا."), "index.html#start")}
<div id="start"></div>'''
AR["nav_home"] = "الرئيسية"; AR["nav_ins"] = "رؤى درج"
FILTER_JS = """<script>
document.querySelectorAll('#pills button').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('#pills button').forEach(x => x.classList.toggle('on', x === b));
  const f = b.dataset.f;
  document.querySelectorAll('#grid > *').forEach(c => { c.hidden = !(f === 'all' || c.dataset.cat === f); });
}));
</script>"""
build("daraj-insights.html", "nav_ins", "Daraj Insights — Practical ideas for money and business", "Short, honest articles on growth, cash, deals and AI for owners and investors.", ins, extra_js=FILTER_JS)

# ===== ARTICLES =====
WA_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.4-4.3a8.5 8.5 0 1 1 15.6-4.5z"></path></svg>'
for idx, A in enumerate(ARTICLES):
    AR.clear()
    a = ARTS[idx]
    X = A["extra"]
    body_parts = []; toc = []
    for j, it in enumerate(A["body"]):
        if it[0] == "p": body_parts.append(t(f"ab{j}", it[1], it[2], "p"))
        elif it[0] == "h":
            body_parts.append(t(f"ab{j}", it[1], it[2], "h2", f'id="s{j}"'))
            toc.append(f'<li><a href="#s{j}" data-i18n="tc{j}">{it[1]}</a></li>'); AR[f"tc{j}"] = it[2]
        elif it[0] == "q": body_parts.append(t(f"ab{j}", it[1], it[2], "blockquote"))
        elif it[0] == "ul": body_parts.append("<ul>" + "".join(t(f"ab{j}_{n}", e, r, "li") for n, (e, r) in enumerate(it[1])) + "</ul>")
    tk = '<div class="tk">' + t("tk_h", "Key takeaways", "أبرز النقاط", "b") + "<ul>" + "".join(t(f"tk{n}", e, r, "li") for n, (e, r) in enumerate(X["tk"])) + "</ul></div>"
    T_ = X["table"]
    tbl = '<div class="atbl">' + t("tb_h", T_["title"][0], T_["title"][1], "h3") + '<div class="sc"><table><thead><tr>' + "".join(t(f"th{n}", e, r, "th") for n, (e, r) in enumerate(T_["head"])) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(t(f"td{ri}_{ci}", e, r, "td") for ci, (e, r) in enumerate(row)) + "</tr>" for ri, row in enumerate(T_["rows"])) + "</tbody></table></div></div>"
    E_ = X["ex"]
    ex = '<div class="aex">' + t("ex_l", E_[0], E_[1], "span", 'class="lb"') + t("ex_p", E_[2], E_[3], "p") + "</div>"
    fq = '<div class="afaq">' + t("fq_h", "Questions owners ask", "أسئلة شائعة", "h2", 'id="faq"') + "".join("<details>" + t(f"fq{n}q", q, qa, "summary") + t(f"fq{n}a", an, aa, "p") + "</details>" for n, (q, qa, an, aa) in enumerate(X["faq"])) + "</div>"
    toc.append('<li><a href="#faq" data-i18n="tcf">Questions owners ask</a></li>'); AR["tcf"] = "أسئلة شائعة"
    mid = len(body_parts) // 2
    hs = [k for k, x in enumerate(body_parts) if "<h2" in x and k >= mid]
    cut = hs[0] if hs else mid
    cov = f'<figure class="acover"><img src="images/{a[10]}.jpg" alt="{a[11]}" data-alt-ar="{a[12]}" width="1600" height="900"></figure>'
    parts = [cov, tk] + body_parts[:cut] + [tbl] + body_parts[cut:] + [ex, fq]
    c = A["cta"]
    endcta = f'''<div class="endcta">{t("ec_k", c[1], c[2], "span", 'class="k"')}{t("ec_h", c[3], c[4], "h2")}{t("ec_p", c[5], c[6], "p")}
 <div class="ctas" style="margin:18px 0 0">{t("ec_b", c[7] + " →", c[8] + " ←", "a", f'class="btn btn-gold" href="{c[0]}"')}{t("ec_w", "Chat on WhatsApp", "تواصل عبر واتساب", "a", 'class="btn btn-line" href="index.html#start" style="color:#fff;border-color:#5B6E8C"')}</div>
 {t("ec_n", "Free · no obligation · reply within one working day", "مجانًا · بدون أي التزام · نرد خلال يوم عمل واحد", "p", 'class="n"')}</div>'''
    same = [x for x in ARTS if x[0] != a[0] and x[7] == a[7]]
    others = (same + [x for x in ARTS if x[0] != a[0] and x not in same])[:3]
    body = f'''<div class="crumb"><div class="wrap"><a href="index.html" data-i18n="nav_home">Home</a> / <a href="daraj-insights.html" data-i18n="nav_ins">Articles</a> / <span style="color:#fff" data-i18n="a_cat">{a[1]}</span></div></div>
<section class="hero" id="top" style="padding:56px 0 48px"><div class="wrap" style="max-width:860px">
 {t("a_eb", a[1] + " · " + a[8], a[2] + " · " + a[9], "div", 'class="eyebrow" style="color:var(--gold)"')}
 {t("a_h1", a[3], a[4], "h1", 'style="font-size:clamp(28px,3.4vw,40px);line-height:1.2;margin-top:12px"')}
 {t("a_ld", a[5], a[6], "p", 'class="lead" style="font-size:18px;max-width:720px"')}
 {t("a_by", "By the Daraj team · [Publication date]", "فريق درج · [تاريخ النشر]", "p", 'style="color:#C9D2DE;font-size:14px;margin:0"')}
</div></section>
<section style="padding-top:48px"><div class="wrap artw">
 <article class="prose">{"".join(parts)}{endcta}</article>
 <aside>
  <nav class="toc" aria-label="Contents">{t("tc_h","In this article","محتويات المقال","b")}<ol>{"".join(toc)}</ol></nav>
  <div class="side">{t("sd_k", c[1], c[2], "span", 'style="color:var(--gold);font-weight:700;font-size:13px"')}{t("sd_h", c[3], c[4], "h3", 'style="font-size:22px"')}{t("sd_p", c[5], c[6], "p")}<div>{t("sd_b", c[7], c[8], "a", f'class="btn btn-gold" href="{c[0]}"')}</div></div>
  <div style="background:#fff;border:1px solid var(--line);border-radius:20px;padding:24px">{t("sh_h","Share this article","شارك المقال","b")}<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px"><a class="btn btn-line" style="min-height:40px;padding:8px 14px;font-size:14px" href="#">LinkedIn</a><a class="btn btn-line" style="min-height:40px;padding:8px 14px;font-size:14px" href="#">WhatsApp</a></div></div>
 </aside>
</div></section>
<section class="ivory"><div class="wrap"><div class="sec-head">{t("mo_h","Keep reading","مقالات ذات صلة","h2")}</div><div class="ins">{art_cards("mo", items=others)}</div></div></section>
{band("ab", ("Do you need expert advice on your business?","هل تحتاج إلى رأي متخصص في مشروعك؟"), ("Book a free call with one of our senior advisors. One hour, with no obligation.","احجز مكالمة مجانية مع أحد كبار مستشارينا، لمدة ساعة ودون أي التزام."), "index.html#start")}
<div id="start"></div>'''
    AR["nav_home"] = "الرئيسية"; AR["nav_ins"] = "المقالات"; AR["a_cat"] = a[2]
    build(a[0], "nav_ins", f"{a[3]} — Daraj Insights", a[5], body)

# nav: make door headings link to the door pages, in every page
for f in os.listdir(OUT):
    if not f.endswith(".html"): continue
    p = os.path.join(OUT, f); h = open(p, encoding="utf-8").read()
    h = re.sub(r'<h4([^>]*)data-i18n="div_invest">(.*?)</h4>', r'<h4><a href="daraj-invest.html" style="color:inherit"\1data-i18n="div_invest">\2</a></h4>', h)
    h = h.replace('href="daraj-departments.html#senior"', 'href="daraj-private-advisory.html"').replace('"s_adv": "الاستشارة الخاصة"', '"s_adv": "الاستشارات الخاصة"')
    h = re.sub(r'<h4([^>]*)data-i18n="div_bs">(.*?)</h4>', r'<h4><a href="daraj-business.html" style="color:inherit"\1data-i18n="div_bs">\2</a></h4>', h)
    open(p, "w", encoding="utf-8").write(h)
print("all pages done")
