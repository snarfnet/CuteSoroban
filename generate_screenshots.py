"""Generate App Store screenshots for multiple apps using PIL."""
import os
from PIL import Image, ImageDraw, ImageFont

BOLD = "C:/Windows/Fonts/meiryob.ttc"
REGULAR = "C:/Windows/Fonts/meiryo.ttc"

SIZES = {
    "iphone67": (1290, 2796),
    "iphone65": (1242, 2688),
    "iphone55": (1242, 2208),
    "ipad129":  (2048, 2732),
}

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)

def draw_status_bar(draw, w, color=(255,255,255)):
    draw.text((60, 18), "9:41", fill=color, font=font(32))
    # signal dots
    for i in range(4):
        draw.ellipse([w-200+i*18, 24, w-200+i*18+10, 34], fill=color)
    draw.text((w-140, 18), "100%", fill=color, font=font(28))

def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_pill(draw, xy, fill):
    draw.rounded_rectangle(xy, radius=999, fill=fill)

def create_gradient(w, h, top_color, bottom_color):
    img = Image.new("RGB", (w, h))
    for y in range(h):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / h)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / h)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / h)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img

def create_gradient_fast(w, h, top_color, bottom_color):
    """Faster gradient using line-by-line approach."""
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / h)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / h)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img, draw

# ============================================================
# MimiNenrei - Ear Age Test
# ============================================================
def gen_miminenrei(size_name, w, h):
    imgs = []
    s = w / 1290  # scale factor

    # SS1: Home screen
    img, draw = create_gradient_fast(w, h, (15, 10, 40), (5, 5, 20))
    draw_status_bar(draw, w)
    # Title
    draw.text((w//2-int(250*s), int(350*s)), "みみ年齢", fill=(255,255,255), font=font(int(90*s)), anchor=None)
    draw.text((w//2-int(200*s), int(480*s)), "MimiNenrei", fill=(180,130,255), font=font(int(40*s)))
    # Ear icon area
    cx, cy = w//2, int(900*s)
    draw_rounded_rect(draw, [cx-int(180*s), cy-int(180*s), cx+int(180*s), cy+int(180*s)], int(90*s), (60, 30, 120))
    draw.text((cx-int(60*s), cy-int(50*s)), "👂", fill=(255,255,255), font=font(int(100*s)))
    # Description
    draw.text((w//2-int(350*s), int(1250*s)), "あなたの耳年齢を\n簡単にテストできます", fill=(200,200,220), font=font(int(44*s), False))
    # Start button
    draw_rounded_rect(draw, [int(200*s), int(1550*s), w-int(200*s), int(1700*s)], int(24*s), (140, 80, 255))
    draw.text((w//2-int(180*s), int(1580*s)), "テストを開始する", fill=(255,255,255), font=font(int(48*s)))
    # Ad bar
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (20, 20, 30))
    draw.text((w//2-int(80*s), h-int(90*s)), "広告エリア", fill=(100,100,120), font=font(int(28*s), False))
    imgs.append(img)

    # SS2: Test in progress
    img, draw = create_gradient_fast(w, h, (15, 10, 40), (5, 5, 20))
    draw_status_bar(draw, w)
    draw.text((w//2-int(200*s), int(200*s)), "周波数テスト中", fill=(255,255,255), font=font(int(56*s)))
    draw.text((w//2-int(120*s), int(320*s)), "8,000 Hz", fill=(140, 200, 255), font=font(int(72*s)))
    # Waveform visualization
    import math
    for i in range(int(800*s)):
        x = int(100*s) + i
        amp = int(80*s) * math.sin(i * 0.05) * math.sin(i * 0.002)
        y = int(700*s)
        draw.line([(x, y-abs(int(amp))), (x, y+abs(int(amp)))], fill=(140, 80, 255), width=2)
    # Progress
    draw.text((w//2-int(100*s), int(1000*s)), "進行度", fill=(180,180,200), font=font(int(36*s), False))
    draw_rounded_rect(draw, [int(200*s), int(1080*s), w-int(200*s), int(1120*s)], int(20*s), (40, 40, 60))
    draw_rounded_rect(draw, [int(200*s), int(1080*s), int(200*s)+(w-int(400*s))*6//10, int(1120*s)], int(20*s), (140, 80, 255))
    # Buttons
    draw_rounded_rect(draw, [int(300*s), int(1300*s), w//2-int(30*s), int(1480*s)], int(24*s), (60, 180, 80))
    draw.text((int(370*s), int(1360*s)), "聞こえる", fill=(255,255,255), font=font(int(44*s)))
    draw_rounded_rect(draw, [w//2+int(30*s), int(1300*s), w-int(300*s), int(1480*s)], int(24*s), (200, 60, 60))
    draw.text((w//2+int(100*s), int(1360*s)), "聞こえない", fill=(255,255,255), font=font(int(44*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (20, 20, 30))
    imgs.append(img)

    # SS3: Result screen
    img, draw = create_gradient_fast(w, h, (15, 10, 40), (5, 5, 20))
    draw_status_bar(draw, w)
    draw.text((w//2-int(140*s), int(250*s)), "テスト結果", fill=(255,255,255), font=font(int(64*s)))
    # Age circle
    cx, cy = w//2, int(650*s)
    draw_rounded_rect(draw, [cx-int(200*s), cy-int(200*s), cx+int(200*s), cy+int(200*s)], int(200*s), (60, 30, 120))
    draw.text((cx-int(80*s), cy-int(90*s)), "28", fill=(140, 200, 255), font=font(int(130*s)))
    draw.text((cx-int(30*s), cy+int(60*s)), "歳", fill=(200, 200, 220), font=font(int(48*s)))
    draw.text((w//2-int(180*s), int(950*s)), "あなたのみみ年齢", fill=(180,180,200), font=font(int(40*s), False))
    # Result details
    draw_rounded_rect(draw, [int(120*s), int(1100*s), w-int(120*s), int(1500*s)], int(20*s), (30, 20, 60))
    draw.text((int(180*s), int(1150*s)), "最高可聴周波数: 14,000 Hz", fill=(200,200,220), font=font(int(38*s), False))
    draw.text((int(180*s), int(1240*s)), "判定: 若々しい耳です!", fill=(100, 220, 140), font=font(int(38*s)))
    draw.text((int(180*s), int(1340*s)), "同年代の平均: 12,500 Hz", fill=(180,180,200), font=font(int(34*s), False))
    # Retry button
    draw_rounded_rect(draw, [int(200*s), int(1600*s), w-int(200*s), int(1750*s)], int(24*s), (140, 80, 255))
    draw.text((w//2-int(140*s), int(1630*s)), "もう一度テスト", fill=(255,255,255), font=font(int(48*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (20, 20, 30))
    imgs.append(img)

    return imgs

# ============================================================
# DRIFT Techno Engine
# ============================================================
def gen_drift(size_name, w, h):
    imgs = []
    s = w / 1290

    # SS1: Main screen
    img, draw = create_gradient_fast(w, h, (5, 5, 15), (10, 5, 25))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "DRIFT", fill=(0, 255, 180), font=font(int(80*s)))
    draw.text((int(60*s), int(230*s)), "Techno Engine", fill=(100, 100, 120), font=font(int(36*s)))
    # Waveform display
    draw_rounded_rect(draw, [int(40*s), int(380*s), w-int(40*s), int(680*s)], int(16*s), (15, 15, 30))
    import math
    for i in range(int(1100*s)):
        x = int(80*s) + i
        amp = int(100*s) * math.sin(i * 0.03) * (0.5 + 0.5 * math.sin(i * 0.008))
        y = int(530*s)
        draw.line([(x, y-abs(int(amp))), (x, y+abs(int(amp)))], fill=(0, 255, 180), width=2)
    # Knobs row
    for i in range(4):
        cx = int(180*s) + i * int(280*s)
        cy = int(900*s)
        draw_rounded_rect(draw, [cx-int(60*s), cy-int(60*s), cx+int(60*s), cy+int(60*s)], int(60*s), (30, 30, 50))
        labels = ["TEMPO", "REVERB", "DELAY", "FILTER"]
        draw.text((cx-int(45*s), cy+int(75*s)), labels[i], fill=(0, 255, 180), font=font(int(22*s)))
    # Pads grid
    for r in range(2):
        for c in range(4):
            x = int(80*s) + c * int(290*s)
            y = int(1150*s) + r * int(240*s)
            color = (0, int(180+r*30), int(120+c*20))
            draw_rounded_rect(draw, [x, y, x+int(250*s), y+int(200*s)], int(16*s), color)
    # Play button
    draw_rounded_rect(draw, [int(200*s), int(1750*s), w-int(200*s), int(1900*s)], int(24*s), (0, 255, 180))
    draw.text((w//2-int(50*s), int(1780*s)), "PLAY", fill=(0, 0, 0), font=font(int(48*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10, 10, 20))
    imgs.append(img)

    # SS2: Sequencer
    img, draw = create_gradient_fast(w, h, (5, 5, 15), (10, 5, 25))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "SEQUENCER", fill=(0, 255, 180), font=font(int(56*s)))
    # Grid
    for r in range(8):
        for c in range(16):
            x = int(40*s) + c * int(74*s)
            y = int(300*s) + r * int(90*s)
            active = (r + c) % 3 == 0
            color = (0, 200, 150) if active else (25, 25, 40)
            draw_rounded_rect(draw, [x, y, x+int(66*s), y+int(78*s)], int(8*s), color)
    # BPM display
    draw_rounded_rect(draw, [int(40*s), int(1120*s), w-int(40*s), int(1280*s)], int(16*s), (15, 15, 30))
    draw.text((int(100*s), int(1150*s)), "BPM", fill=(100,100,120), font=font(int(36*s)))
    draw.text((int(260*s), int(1140*s)), "128", fill=(0, 255, 180), font=font(int(72*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10, 10, 20))
    imgs.append(img)

    # SS3: Effects
    img, draw = create_gradient_fast(w, h, (5, 5, 15), (10, 5, 25))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "EFFECTS", fill=(0, 255, 180), font=font(int(56*s)))
    # Effect sliders
    effects = ["REVERB", "DELAY", "DISTORTION", "CHORUS", "FILTER", "PHASER"]
    for i, name in enumerate(effects):
        y = int(320*s) + i * int(180*s)
        draw.text((int(80*s), y), name, fill=(0, 255, 180), font=font(int(30*s)))
        draw_rounded_rect(draw, [int(80*s), y+int(50*s), w-int(80*s), y+int(70*s)], int(10*s), (25, 25, 40))
        val = [0.7, 0.4, 0.2, 0.6, 0.8, 0.3][i]
        draw_rounded_rect(draw, [int(80*s), y+int(50*s), int(80*s)+int((w-int(160*s))*val), y+int(70*s)], int(10*s), (0, 255, 180))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10, 10, 20))
    imgs.append(img)

    return imgs

# ============================================================
# ShinreiSpot - Ghost Radar
# ============================================================
def gen_shinreispot(size_name, w, h):
    imgs = []
    s = w / 1290
    red = (235, 33, 46)
    dark_red = (60, 10, 15)

    # SS1: List view
    img, draw = create_gradient_fast(w, h, (10, 10, 18), (4, 4, 7))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "GPS近隣心霊スポット", fill=(255,255,255), font=font(int(52*s)))
    # Search bar
    draw_rounded_rect(draw, [int(60*s), int(240*s), w-int(60*s), int(320*s)], int(14*s), (30,30,40))
    draw.text((int(90*s), int(255*s)), "スポット名・都道府県で検索", fill=(100,100,120), font=font(int(30*s), False))
    # Category pills
    cats = ["すべて", "廃墟", "トンネル", "橋", "病院", "山"]
    cx = int(60*s)
    for cat in cats:
        tw = len(cat) * int(36*s) + int(30*s)
        sel = cat == "すべて"
        draw_pill(draw, [cx, int(360*s), cx+tw, int(410*s)], red if sel else (30,30,40))
        draw.text((cx+int(15*s), int(365*s)), cat, fill=(255,255,255) if sel else (150,150,160), font=font(int(26*s)))
        cx += tw + int(16*s)
    # Spot cards
    spots = [("青木ヶ原樹海", "山梨県", "山", "★★★★★", "1.2 km"),
             ("犬鳴トンネル", "福岡県", "トンネル", "★★★★★", "3.5 km"),
             ("八王子城跡", "東京都", "廃墟", "★★★★", "5.8 km")]
    for i, (name, pref, cat, lv, dist) in enumerate(spots):
        y = int(470*s) + i * int(240*s)
        draw_rounded_rect(draw, [int(60*s), y, w-int(60*s), y+int(210*s)], int(18*s), (15,15,25))
        draw_rounded_rect(draw, [int(80*s), y+int(20*s), int(150*s), y+int(90*s)], int(15*s), dark_red)
        draw.text((int(170*s), y+int(20*s)), name, fill=(255,255,255), font=font(int(38*s)))
        draw.text((int(170*s), y+int(80*s)), f"{pref}  {cat}", fill=(180,180,190), font=font(int(26*s), False))
        draw.text((w-int(200*s), y+int(20*s)), dist, fill=red, font=font(int(30*s)))
        draw.text((int(170*s), y+int(130*s)), lv, fill=red, font=font(int(28*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,15))
    imgs.append(img)

    # SS2: Radar view
    img, draw = create_gradient_fast(w, h, (10, 10, 18), (4, 4, 7))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "心霊レーダー", fill=(255,255,255), font=font(int(52*s)))
    # Radar circles
    cx, cy = w//2, int(1100*s)
    import math
    for ring in range(1, 5):
        r = int(ring * 180 * s)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(60, 15, 20), width=2)
    # Crosshairs
    draw.line([(cx, cy-int(720*s)), (cx, cy+int(720*s))], fill=(60,15,20), width=1)
    draw.line([(cx-int(720*s), cy), (cx+int(720*s), cy)], fill=(60,15,20), width=1)
    # Sweep area
    for a in range(30):
        angle = math.radians(45 - a)
        x2 = cx + int(700*s * math.cos(angle))
        y2 = cy - int(700*s * math.sin(angle))
        alpha = int(235 * (1 - a/30))
        draw.line([(cx, cy), (x2, y2)], fill=(alpha, int(alpha*0.14), int(alpha*0.18)), width=2)
    # Blips
    blips = [(200, -300, 14), (-350, 100, 10), (100, 400, 18), (-200, -150, 12)]
    for bx, by, bs in blips:
        px, py = cx+int(bx*s), cy+int(by*s)
        draw.ellipse([px-int(bs*s), py-int(bs*s), px+int(bs*s), py+int(bs*s)], fill=(235, 33, 46, 180))
    # Center
    draw.ellipse([cx-int(8*s), cy-int(8*s), cx+int(8*s), cy+int(8*s)], fill=(0, 200, 0))
    draw.text((w//2-int(100*s), h-int(250*s)), "検出: 4件", fill=(200,60,60), font=font(int(28*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,15))
    imgs.append(img)

    # SS3: Detail view
    img, draw = create_gradient_fast(w, h, (10, 10, 18), (4, 4, 7))
    draw_status_bar(draw, w)
    # Map area placeholder
    draw_rounded_rect(draw, [int(60*s), int(120*s), w-int(60*s), int(600*s)], int(18*s), (30, 40, 35))
    draw.text((w//2-int(60*s), int(340*s)), "MAP", fill=(100,120,110), font=font(int(48*s)))
    # Pin
    draw.ellipse([w//2-int(20*s), int(300*s), w//2+int(20*s), int(340*s)], fill=red)
    # Detail
    draw.text((int(80*s), int(660*s)), "青木ヶ原樹海", fill=(255,255,255), font=font(int(56*s)))
    draw.text((int(80*s), int(760*s)), "山梨県  山  1.2 km", fill=(180,180,190), font=font(int(30*s), False))
    # Danger level
    draw.text((int(80*s), int(860*s)), "危険度", fill=(180,180,190), font=font(int(32*s), False))
    for i in range(5):
        c = red if i < 5 else (40,40,50)
        draw.text((int(230*s)+i*int(50*s), int(850*s)), "🔥", fill=c, font=font(int(40*s)))
    # Description
    draw.text((int(80*s), int(980*s)), "富士山麓に広がる広大な原生林。\n自殺の名所として知られ、\n多くの霊が彷徨うとされる。", fill=(200,200,210), font=font(int(36*s), False))
    # Open in maps button
    draw_rounded_rect(draw, [int(80*s), int(1300*s), w-int(80*s), int(1420*s)], int(16*s), (180, 25, 35))
    draw.text((w//2-int(150*s), int(1330*s)), "マップで開く", fill=(255,255,255), font=font(int(40*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,15))
    imgs.append(img)

    return imgs

# ============================================================
# MagazineStand
# ============================================================
def gen_magazinestand(size_name, w, h):
    imgs = []
    s = w / 1290

    # SS1: Main shelf
    img, draw = create_gradient_fast(w, h, (18, 18, 28), (8, 8, 15))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "マガジンスタンド", fill=(255,255,255), font=font(int(56*s)))
    draw.text((int(60*s), int(210*s)), "メイン棚", fill=(255, 180, 50), font=font(int(32*s)))
    # Magazine covers grid
    colors = [(200,50,50),(50,100,200),(50,180,80),(200,150,30),(150,50,200),(200,100,50)]
    titles = ["週刊文春", "FRIDAY", "AERA", "東洋経済", "Newswk", "Number"]
    for r in range(2):
        for c in range(3):
            x = int(60*s) + c * int(390*s)
            y = int(340*s) + r * int(520*s)
            draw_rounded_rect(draw, [x, y, x+int(360*s), y+int(480*s)], int(12*s), colors[r*3+c])
            draw.text((x+int(20*s), y+int(380*s)), titles[r*3+c], fill=(255,255,255), font=font(int(34*s)))
            draw.text((x+int(20*s), y+int(20*s)), "最新号", fill=(255,255,255,180), font=font(int(24*s)))
    # Bottom tab bar
    draw_rounded_rect(draw, [0, h-int(180*s), w, h], 0, (20, 20, 30))
    tabs = ["メイン棚", "スキャン", "カレンダー", "統計"]
    icons = ["📖", "📷", "📅", "📊"]
    for i, (tab, icon) in enumerate(zip(tabs, icons)):
        tx = int(80*s) + i * int(300*s)
        sel = i == 0
        draw.text((tx+int(30*s), h-int(160*s)), icon, font=font(int(36*s)))
        draw.text((tx, h-int(110*s)), tab, fill=(255,180,50) if sel else (120,120,130), font=font(int(24*s)))
    imgs.append(img)

    # SS2: Barcode scanner
    img, draw = create_gradient_fast(w, h, (18, 18, 28), (8, 8, 15))
    draw_status_bar(draw, w)
    draw.text((w//2-int(200*s), int(120*s)), "バーコードスキャン", fill=(255,255,255), font=font(int(50*s)))
    # Camera viewfinder
    draw_rounded_rect(draw, [int(100*s), int(400*s), w-int(100*s), int(1200*s)], int(20*s), (25,25,35))
    # Scan frame
    frame_m = int(180*s)
    draw.rectangle([frame_m, int(600*s), frame_m+int(100*s), int(602*s)], fill=(255,180,50))
    draw.rectangle([frame_m, int(600*s), frame_m+int(2*s), int(700*s)], fill=(255,180,50))
    draw.rectangle([w-frame_m-int(100*s), int(600*s), w-frame_m, int(602*s)], fill=(255,180,50))
    draw.rectangle([w-frame_m-int(2*s), int(600*s), w-frame_m, int(700*s)], fill=(255,180,50))
    draw.rectangle([frame_m, int(998*s), frame_m+int(100*s), int(1000*s)], fill=(255,180,50))
    draw.rectangle([frame_m, int(900*s), frame_m+int(2*s), int(1000*s)], fill=(255,180,50))
    draw.rectangle([w-frame_m-int(100*s), int(998*s), w-frame_m, int(1000*s)], fill=(255,180,50))
    draw.rectangle([w-frame_m-int(2*s), int(900*s), w-frame_m, int(1000*s)], fill=(255,180,50))
    # Scan line
    draw.rectangle([frame_m+int(10*s), int(790*s), w-frame_m-int(10*s), int(794*s)], fill=(255,180,50))
    draw.text((w//2-int(250*s), int(1300*s)), "雑誌のバーコードを\nスキャンしてください", fill=(180,180,190), font=font(int(40*s), False))
    draw_rounded_rect(draw, [0, h-int(180*s), w, h], 0, (20, 20, 30))
    for i, (tab, icon) in enumerate(zip(tabs, icons)):
        tx = int(80*s) + i * int(300*s)
        sel = i == 1
        draw.text((tx+int(30*s), h-int(160*s)), icon, font=font(int(36*s)))
        draw.text((tx, h-int(110*s)), tab, fill=(255,180,50) if sel else (120,120,130), font=font(int(24*s)))
    imgs.append(img)

    # SS3: Stats
    img, draw = create_gradient_fast(w, h, (18, 18, 28), (8, 8, 15))
    draw_status_bar(draw, w)
    draw.text((w//2-int(60*s), int(120*s)), "統計", fill=(255,255,255), font=font(int(56*s)))
    # Bar chart
    draw.text((int(60*s), int(300*s)), "月別購読数", fill=(200,200,210), font=font(int(36*s)))
    months = ["1月", "2月", "3月", "4月", "5月", "6月"]
    vals = [4, 6, 3, 8, 5, 7]
    max_v = max(vals)
    for i, (m, v) in enumerate(zip(months, vals)):
        x = int(120*s) + i * int(180*s)
        bh = int(v / max_v * 400 * s)
        y = int(900*s) - bh
        draw_rounded_rect(draw, [x, y, x+int(100*s), int(900*s)], int(8*s), (255, 180, 50))
        draw.text((x+int(15*s), int(930*s)), m, fill=(180,180,190), font=font(int(24*s), False))
        draw.text((x+int(30*s), y-int(40*s)), str(v), fill=(255,255,255), font=font(int(28*s)))
    # Summary cards
    draw_rounded_rect(draw, [int(60*s), int(1050*s), w//2-int(30*s), int(1250*s)], int(16*s), (30,30,45))
    draw.text((int(100*s), int(1090*s)), "総購読数", fill=(180,180,190), font=font(int(28*s), False))
    draw.text((int(100*s), int(1150*s)), "33冊", fill=(255,255,255), font=font(int(52*s)))
    draw_rounded_rect(draw, [w//2+int(30*s), int(1050*s), w-int(60*s), int(1250*s)], int(16*s), (30,30,45))
    draw.text((w//2+int(70*s), int(1090*s)), "今月", fill=(180,180,190), font=font(int(28*s), False))
    draw.text((w//2+int(70*s), int(1150*s)), "7冊", fill=(255,180,50), font=font(int(52*s)))
    draw_rounded_rect(draw, [0, h-int(180*s), w, h], 0, (20, 20, 30))
    for i, (tab, icon) in enumerate(zip(tabs, icons)):
        tx = int(80*s) + i * int(300*s)
        sel = i == 3
        draw.text((tx+int(30*s), h-int(160*s)), icon, font=font(int(36*s)))
        draw.text((tx, h-int(110*s)), tab, fill=(255,180,50) if sel else (120,120,130), font=font(int(24*s)))
    imgs.append(img)

    return imgs

# ============================================================
# EigaMachineGun - Movie Info (iPad only needed)
# ============================================================
def gen_eigamachinegun(size_name, w, h):
    imgs = []
    s = w / 1290 if size_name != "ipad129" else w / 2048

    # SS1: Movie list
    img, draw = create_gradient_fast(w, h, (12, 12, 20), (5, 5, 12))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "映画マシンガン", fill=(255,255,255), font=font(int(60*s)))
    draw.text((int(60*s), int(220*s)), "MOVIE MACHINEGUN", fill=(255, 60, 60), font=font(int(28*s)))
    # Movie cards
    movies = [
        ("千と千尋の神隠し", "宮崎駿", "2001", (180,50,50)),
        ("君の名は。", "新海誠", "2016", (50,80,180)),
        ("鬼滅の刃", "外崎春雄", "2020", (50,150,80)),
        ("スラムダンク", "井上雄彦", "2022", (200,130,30)),
    ]
    for i, (title, director, year, color) in enumerate(movies):
        y = int(340*s) + i * int(280*s)
        # Poster placeholder
        draw_rounded_rect(draw, [int(60*s), y, int(250*s), y+int(250*s)], int(12*s), color)
        draw.text((int(100*s), y+int(90*s)), "🎬", font=font(int(60*s)))
        # Info
        draw.text((int(280*s), y+int(20*s)), title, fill=(255,255,255), font=font(int(42*s)))
        draw.text((int(280*s), y+int(80*s)), f"監督: {director}", fill=(180,180,190), font=font(int(28*s), False))
        draw.text((int(280*s), y+int(130*s)), year, fill=(255,60,60), font=font(int(32*s)))
        # Rating stars
        draw.text((int(280*s), y+int(180*s)), "★★★★☆", fill=(255,200,50), font=font(int(32*s)))
    # Speed slider
    draw_rounded_rect(draw, [int(60*s), int(1500*s), w-int(60*s), int(1600*s)], int(16*s), (25,25,35))
    draw.text((int(100*s), int(1520*s)), "速度", fill=(180,180,190), font=font(int(28*s), False))
    draw_rounded_rect(draw, [int(250*s), int(1540*s), w-int(100*s), int(1560*s)], int(10*s), (40,40,55))
    draw_rounded_rect(draw, [int(250*s), int(1540*s), int(700*s), int(1560*s)], int(10*s), (255, 60, 60))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,18))
    imgs.append(img)

    # SS2: Movie detail
    img, draw = create_gradient_fast(w, h, (12, 12, 20), (5, 5, 12))
    draw_status_bar(draw, w)
    # Hero poster
    draw_rounded_rect(draw, [0, int(80*s), w, int(650*s)], 0, (180, 50, 50))
    draw.text((w//2-int(80*s), int(300*s)), "🎬", font=font(int(120*s)))
    # Title
    draw.text((int(60*s), int(700*s)), "千と千尋の神隠し", fill=(255,255,255), font=font(int(56*s)))
    draw.text((int(60*s), int(790*s)), "Spirited Away (2001)", fill=(180,180,190), font=font(int(32*s), False))
    draw.text((int(60*s), int(860*s)), "★★★★★  8.6/10", fill=(255,200,50), font=font(int(36*s)))
    # Info
    draw_rounded_rect(draw, [int(60*s), int(960*s), w-int(60*s), int(1400*s)], int(16*s), (20,20,32))
    draw.text((int(100*s), int(1000*s)), "監督: 宮崎駿", fill=(200,200,210), font=font(int(34*s), False))
    draw.text((int(100*s), int(1060*s)), "ジャンル: アニメ / ファンタジー", fill=(200,200,210), font=font(int(34*s), False))
    draw.text((int(100*s), int(1120*s)), "上映時間: 125分", fill=(200,200,210), font=font(int(34*s), False))
    draw.text((int(100*s), int(1200*s)), "千尋は不思議な町に迷い込み、\n両親を助けるため湯屋で\n働くことになる...", fill=(180,180,190), font=font(int(32*s), False))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,18))
    imgs.append(img)

    # SS3: Search
    img, draw = create_gradient_fast(w, h, (12, 12, 20), (5, 5, 12))
    draw_status_bar(draw, w)
    draw.text((int(60*s), int(120*s)), "映画を探す", fill=(255,255,255), font=font(int(56*s)))
    draw_rounded_rect(draw, [int(60*s), int(250*s), w-int(60*s), int(330*s)], int(14*s), (30,30,42))
    draw.text((int(90*s), int(265*s)), "タイトルで検索...", fill=(100,100,120), font=font(int(30*s), False))
    # Genre tags
    genres = ["アクション", "SF", "ホラー", "コメディ", "アニメ", "ドラマ"]
    gx = int(60*s)
    for g in genres:
        tw = len(g) * int(36*s) + int(30*s)
        draw_pill(draw, [gx, int(380*s), gx+tw, int(435*s)], (255, 60, 60))
        draw.text((gx+int(15*s), int(388*s)), g, fill=(255,255,255), font=font(int(28*s)))
        gx += tw + int(12*s)
    # Trending section
    draw.text((int(60*s), int(520*s)), "トレンド", fill=(255,60,60), font=font(int(40*s)))
    for i in range(3):
        y = int(600*s) + i * int(200*s)
        color = [(50,80,180),(50,150,80),(200,130,30)][i]
        draw_rounded_rect(draw, [int(60*s), y, int(200*s), y+int(170*s)], int(12*s), color)
        titles = ["ゴジラ-1.0", "THE FIRST SLAM DUNK", "すずめの戸締まり"]
        draw.text((int(230*s), y+int(30*s)), titles[i], fill=(255,255,255), font=font(int(38*s)))
        draw.text((int(230*s), y+int(90*s)), "★★★★☆", fill=(255,200,50), font=font(int(28*s)))
    draw_rounded_rect(draw, [0, h-int(120*s), w, h], 0, (10,10,18))
    imgs.append(img)

    return imgs


# ============================================================
# MAIN
# ============================================================
APPS = {
    "MimiNenrei": {
        "gen": gen_miminenrei,
        "dir": "C:/Users/Windows/MimiNenrei/MarketingAssets/Screenshots",
        "sizes": ["iphone67", "iphone65", "iphone55"],
    },
    "DRIFT": {
        "gen": gen_drift,
        "dir": "C:/Users/Windows/DRIFT/MarketingAssets/Screenshots",
        "sizes": ["iphone67", "iphone65", "iphone55"],
    },
    "ShinreiSpot": {
        "gen": gen_shinreispot,
        "dir": "C:/Users/Windows/ShinreiSpot/MarketingAssets/Screenshots",
        "sizes": ["iphone67", "iphone65", "iphone55"],
    },
    "MagazineStand": {
        "gen": gen_magazinestand,
        "dir": "C:/Users/Windows/MagazineStand/MarketingAssets/Screenshots",
        "sizes": ["iphone67", "iphone65", "iphone55"],
    },
    "EigaMachineGun": {
        "gen": gen_eigamachinegun,
        "dir": "C:/Users/Windows/EigaMachineGun/MarketingAssets/Screenshots",
        "sizes": ["iphone67", "iphone65", "iphone55", "ipad129"],
    },
}

for app_name, cfg in APPS.items():
    print(f"\n=== {app_name} ===")
    for size_name in cfg["sizes"]:
        w, h = SIZES[size_name]
        out_dir = os.path.join(cfg["dir"], size_name)
        os.makedirs(out_dir, exist_ok=True)
        screenshots = cfg["gen"](size_name, w, h)
        for i, img in enumerate(screenshots):
            path = os.path.join(out_dir, f"{size_name}_{i+1:02d}.png")
            img.save(path, "PNG")
            print(f"  {size_name}_{i+1:02d}.png ({w}x{h})")

print("\nDone!")
