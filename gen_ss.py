"""Generate polished CuteSoroban App Store screenshots."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BOLD = "C:/Windows/Fonts/meiryob.ttc"
REGULAR = "C:/Windows/Fonts/meiryo.ttc"

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)

SIZES = {
    "iphone_67": (1290, 2796, "screenshots/iphone_67_01.png"),
    "iphone_65": (1242, 2688, "screenshots/iphone_65_01.png"),
    "ipad_129":  (2048, 2732, "screenshots/ipad_129_01.png"),
}

def draw_text_centered(draw, y, text, w, f, fill):
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, y), text, fill=fill, font=f)

def draw_text_shadow(draw, x, y, text, f, fill, shadow=(0,0,0)):
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            draw.text((x+dx, y+dy), text, fill=shadow, font=f)
    draw.text((x, y), text, fill=fill, font=f)

def make_gradient_banner(w, h, color1, color2):
    """Create a gradient banner image."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        a = int(220 - 100 * y / h)  # fade out alpha
        r = int(color1[0] + (color2[0] - color1[0]) * y / h)
        g = int(color1[1] + (color2[1] - color1[1]) * y / h)
        b = int(color1[2] + (color2[2] - color1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b, a))
    return img

def gen_screenshots(size_name, w, h, base_path):
    base_full = os.path.join("C:/Users/Windows/CuteSoroban", base_path)
    if not os.path.exists(base_full):
        print(f"  SKIP {size_name}: base not found")
        return []

    base = Image.open(base_full).convert("RGBA").resize((w, h), Image.LANCZOS)
    s = w / 1290  # scale factor
    results = []

    # --- SS1: Hero shot with title ---
    img = base.copy()
    # Top gradient overlay
    top_banner = make_gradient_banner(w, int(600*s), (220, 140, 180), (255, 200, 220))
    img.paste(Image.alpha_composite(Image.new("RGBA", top_banner.size, (0,0,0,0)), top_banner), (0, 0), top_banner)
    draw = ImageDraw.Draw(img)
    # Title text
    draw_text_centered(draw, int(120*s), "Cute Soroban", w, font(int(90*s)), (180, 50, 100))
    draw_text_centered(draw, int(250*s), "かわいいそろばん", w, font(int(64*s)), (200, 80, 130))
    draw_text_centered(draw, int(370*s), "パステルカラーでかわいく計算", w, font(int(38*s), False), (160, 80, 120))
    # Bottom badge
    bottom_banner = make_gradient_banner(w, int(300*s), (255, 200, 220), (220, 140, 180))
    bottom_banner = bottom_banner.transpose(Image.FLIP_TOP_BOTTOM)
    img.paste(Image.alpha_composite(Image.new("RGBA", bottom_banner.size, (0,0,0,0)), bottom_banner), (0, h-int(300*s)), bottom_banner)
    draw = ImageDraw.Draw(img)
    draw_text_centered(draw, h-int(220*s), "にゃんこサウンド付き 🐱", w, font(int(44*s)), (180, 50, 100))
    results.append(img.convert("RGB"))

    # --- SS2: Feature highlight - touch & sound ---
    img = base.copy()
    # Darken slightly
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 40))
    img = Image.alpha_composite(img, overlay)
    # Center feature card
    card_y = int(800*s)
    card_h = int(600*s)
    card = Image.new("RGBA", (w-int(120*s), card_h), (255, 220, 235, 210))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([0, 0, card.width-1, card.height-1], radius=int(40*s), outline=(200, 100, 150), width=3)
    img.paste(Image.alpha_composite(Image.new("RGBA", card.size, (0,0,0,0)), card), (int(60*s), card_y), card)
    draw = ImageDraw.Draw(img)
    draw_text_centered(draw, card_y+int(50*s), "🐱 にゃん！", w, font(int(80*s)), (200, 60, 100))
    draw_text_centered(draw, card_y+int(180*s), "珠をタッチすると", w, font(int(50*s)), (150, 50, 90))
    draw_text_centered(draw, card_y+int(260*s), "猫の鳴き声が響きます", w, font(int(50*s)), (150, 50, 90))
    draw_text_centered(draw, card_y+int(380*s), "触覚フィードバック対応", w, font(int(36*s), False), (130, 70, 100))
    draw_text_centered(draw, card_y+int(440*s), "リセットボタンで一括クリア", w, font(int(36*s), False), (130, 70, 100))
    results.append(img.convert("RGB"))

    # --- SS3: Educational / real soroban ---
    img = base.copy()
    # Top section
    top_banner = make_gradient_banner(w, int(750*s), (180, 120, 200), (220, 160, 220))
    img.paste(Image.alpha_composite(Image.new("RGBA", top_banner.size, (0,0,0,0)), top_banner), (0, 0), top_banner)
    draw = ImageDraw.Draw(img)
    draw_text_centered(draw, int(100*s), "本物のそろばんを", w, font(int(64*s)), (120, 40, 100))
    draw_text_centered(draw, int(200*s), "スマホで体験", w, font(int(64*s)), (120, 40, 100))
    # Feature bullets
    features = [
        "✦ 13桁のリアルそろばん",
        "✦ 上珠・下珠を指で操作",
        "✦ 計算結果をリアルタイム表示",
        "✦ iPad にも対応",
    ]
    for i, feat in enumerate(features):
        draw_text_centered(draw, int(360*s) + i*int(75*s), feat, w, font(int(38*s), False), (140, 60, 110))
    results.append(img.convert("RGB"))

    return results


os.makedirs("C:/Users/Windows/CuteSoroban/screenshots", exist_ok=True)

for size_name, (w, h, base_path) in SIZES.items():
    print(f"\n=== {size_name} ({w}x{h}) ===")
    screenshots = gen_screenshots(size_name, w, h, base_path)
    for i, img in enumerate(screenshots):
        path = f"C:/Users/Windows/CuteSoroban/screenshots/{size_name}_{i+1:02d}.png"
        img.save(path, "PNG")
        print(f"  {os.path.basename(path)}")

# Also need iphone_55
print("\n=== iphone_55 (1242x2208) ===")
# Scale from iphone_65
ss_65 = gen_screenshots("iphone_65", 1242, 2688, "screenshots/iphone_65_01.png")
for i, img in enumerate(ss_65):
    resized = img.resize((1242, 2208), Image.LANCZOS)
    path = f"C:/Users/Windows/CuteSoroban/screenshots/iphone_55_{i+1:02d}.png"
    resized.save(path, "PNG")
    print(f"  {os.path.basename(path)}")

print("\nDone!")
