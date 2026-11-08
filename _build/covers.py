from PIL import Image, ImageDraw, ImageFilter
import math, os
W, H = 1600, 900
NAVY=(14,35,66); NAVY2=(22,48,90); NAVY3=(30,62,112); GOLD=(212,173,87); GOLDL=(241,230,204)
def base(seed):
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for y in range(H):  # soft vertical gradient
        t = y / H; c = tuple(int(NAVY[i]*(1-t*0.35) + NAVY2[i]*(t*0.35)) for i in range(3)); d.line([(0,y),(W,y)], fill=c)
    # subtle grid
    for x in range(0, W, 80): d.line([(x,0),(x,H)], fill=(20,43,78))
    for y in range(0, H, 80): d.line([(0,y),(W,y)], fill=(20,43,78))
    # signature steps on the right
    bw, gap, x0 = 120, 26, 980
    hs = [220, 340, 470, 610]
    for i, h in enumerate(hs):
        x = x0 + i*(bw+gap); d.rounded_rectangle([x, H-90-h, x+bw, H-90], 14, fill=NAVY3 if i == 3 else NAVY2)
    pts = [(x0 + i*(bw+gap) + bw//2, H-90-h) for i, h in enumerate(hs)]
    d.line(pts, fill=GOLD, width=8, joint="curve")
    for i, p in enumerate(pts): r = 16 if i == 3 else 12; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r], fill=GOLD)
    return im, d
def glow(im, cx, cy, r):
    g = Image.new("RGB", (W,H), (0,0,0)); gd = ImageDraw.Draw(g); gd.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(90,70,25))
    g = g.filter(ImageFilter.GaussianBlur(120)); return Image.blend(im, Image.eval(Image.merge("RGB",[Image.eval(c, lambda v: v) for c in g.split()]), lambda v: v), 0.0) if False else Image.composite(im, im, Image.new("L",(W,H),255)) if False else Image.fromarray(__import__("numpy").clip(__import__("numpy").asarray(im).astype(int)+__import__("numpy").asarray(g).astype(int),0,255).astype("uint8"))
def icon(d, kind, cx=470, cy=450):
    s = 1.0
    if kind == "cash":
        for i, (dx, dy) in enumerate([(-90,60),(0,0),(90,60),(0,120)]):
            d.ellipse([cx+dx-85, cy+dy-85-60, cx+dx+85, cy+dy+85-60], fill=GOLD if i!=3 else GOLDL, outline=NAVY, width=8)
            d.ellipse([cx+dx-50, cy+dy-50-60, cx+dx+50, cy+dy+50-60], outline=NAVY, width=6)
    elif kind == "invest":
        d.ellipse([cx-170,cy-200,cx+110,cy+80], outline=GOLD, width=26)
        d.line([(cx+80,cy+50),(cx+230,cy+200)], fill=GOLD, width=44)
        for i,h in enumerate([60,110,160]): d.rounded_rectangle([cx-110+i*60, cy+20-h, cx-70+i*60, cy+20], 6, fill=GOLDL)
    elif kind == "sell":
        d.ellipse([cx-210,cy-140,cx-30,cy+40], outline=GOLD, width=34)
        d.line([(cx-40,cy-50),(cx+230,cy-50)], fill=GOLD, width=40)
        for x in (cx+120, cx+190): d.line([(x,cy-50),(x,cy+30)], fill=GOLD, width=36)
    elif kind == "bedaya":
        def leaf(x0,y0,x1,y1,col,flip):
            pts=[]
            for k in range(41):
                t=k/40; x=x0+(x1-x0)*t; y=y0+(y1-y0)*t
                off=math.sin(math.pi*t)*70*(1 if flip else -1)
                nx,ny=-(y1-y0),(x1-x0); L=math.hypot(nx,ny); pts.append((x+nx/L*off,y+ny/L*off))
            for k in range(40,-1,-1):
                t=k/40; x=x0+(x1-x0)*t; y=y0+(y1-y0)*t
                off=math.sin(math.pi*t)*70*(-1 if flip else 1)*0.15
                nx,ny=-(y1-y0),(x1-x0); L=math.hypot(nx,ny); pts.append((x+nx/L*off,y+ny/L*off))
            d.polygon(pts, fill=col)
        d.line([(cx,cy+200),(cx,cy-80)], fill=GOLD, width=22)
        leaf(cx,cy+40,cx-220,cy-140,GOLD,True)
        leaf(cx,cy-20,cx+210,cy-200,GOLDL,False)
        d.rounded_rectangle([cx-150,cy+190,cx+150,cy+240], 20, fill=NAVY3)
    elif kind == "depts":
        for r in range(3):
            for c in range(3):
                x = cx-210+c*150; y = cy-210+r*150
                d.rounded_rectangle([x,y,x+120,y+120], 18, fill=GOLD if (r+c)%2==0 else GOLDL)
        for r in range(3): d.line([(cx-150, cy-150+r*150),(cx+150, cy-150+r*150)], fill=NAVY, width=8)
    elif kind == "ai":
        def gear(x,y,R,teeth,col):
            for k in range(teeth):
                a = 2*math.pi*k/teeth
                d.line([(x+math.cos(a)*R*0.7,y+math.sin(a)*R*0.7),(x+math.cos(a)*R*1.15,y+math.sin(a)*R*1.15)], fill=col, width=int(R*0.35))
            d.ellipse([x-R,y-R,x+R,y+R], fill=col); d.ellipse([x-R*0.38,y-R*0.38,x+R*0.38,y+R*0.38], fill=NAVY)
        gear(cx-60, cy+30, 150, 10, GOLD); gear(cx+170, cy-150, 90, 8, GOLDL)
        d.polygon([(cx+150,cy+140),(cx+190,cy+60),(cx+170,cy+120),(cx+220,cy+110),(cx+170,cy+210),(cx+190,cy+140)], fill=GOLDL)
    elif kind == "pricing":
        d.polygon([(cx-230,cy-120),(cx+60,cy-120),(cx+200,cy+20),(cx+60,cy+160),(cx-230,cy+160)], fill=GOLD)
        d.ellipse([cx+40,cy-10,cx+90,cy+40], fill=NAVY)
        for i,w in enumerate([200,150,170]): d.rounded_rectangle([cx-190,cy-60+i*60,cx-190+w,cy-36+i*60], 10, fill=NAVY)
    elif kind == "capital":
        d.line([(cx-250,cy+170),(cx-20,cy-150)], fill=GOLD, width=34); d.polygon([(cx-60,cy-170),(cx+20,cy-190),(cx+5,cy-110)], fill=GOLD)
        d.line([(cx+210,cy+170),(cx+20,cy-150)], fill=GOLDL, width=34); d.polygon([(cx+60,cy-170),(cx-20,cy-190),(cx-5,cy-110)], fill=GOLDL)
        d.ellipse([cx-30,cy-230,cx+30,cy-170], fill=GOLD)
    elif kind == "friends":
        def person(x, y, sc, col):
            d.ellipse([x-55*sc, y-190*sc, x+55*sc, y-80*sc], fill=col)
            d.rounded_rectangle([x-95*sc, y-60*sc, x+95*sc, y+150*sc], int(60*sc), fill=col)
        person(cx-120, cy+20, 1.0, GOLDL); person(cx+110, cy+20, 1.0, GOLD)
        d.rounded_rectangle([cx-70, cy+40, cx+70, cy+200], 12, fill=(250,247,240), outline=NAVY, width=6)
        for i in range(4): d.line([(cx-45, cy+75+i*30), (cx+45, cy+75+i*30)], fill=NAVY, width=6)
        d.ellipse([cx+40, cy+150, cx+110, cy+220], fill=NAVY); d.text((cx+66, cy+160), "!", fill=GOLD)
        d.rectangle([cx+71, cy+162, cx+79, cy+195], fill=GOLD); d.ellipse([cx+70, cy+201, cx+80, cy+211], fill=GOLD)
os.makedirs("site/images", exist_ok=True)
for k in ["cash","invest","sell","bedaya","depts","ai","pricing","capital","friends"]:
    im, d = base(k)
    im = glow(im, 470, 450, 260); d = ImageDraw.Draw(im)
    icon(d, k)
    im.save(f"site/images/{k}.jpg", quality=86, optimize=True, progressive=True)
print(sorted(os.listdir("site/images")))
