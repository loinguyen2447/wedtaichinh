# Sinh icon cho app WDT AI (chạy bằng python3 + Pillow)
# Kết quả ghi vào ios/WDTAI/Assets.xcassets + icon web (PWA) ở thư mục gốc repo
from PIL import Image, ImageDraw
import os

GOLD = (240, 185, 11)
GREEN = (14, 203, 129)
BG = (13, 17, 23)  # #0d1117
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "WDTAI", "Assets.xcassets")
ROOT = os.path.dirname(HERE)  # thư mục gốc repo


def candle_logo(size, rounded=False):
    """Vẽ logo 3 cây nến: vàng - xanh - vàng trên nền tối."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = size * 14 / 64  # bo góc giống favicon web
    if rounded:
        d.rounded_rectangle([0, 0, size, size], radius=r, fill=BG)
    else:
        d.rectangle([0, 0, size, size], fill=BG)

    # 3 cây nến theo tỉ lệ favicon: x=11..20, 27.5..36.5, 44..53 (trên lưới 64)
    s = size / 64.0
    bars = [
        (int(11 * s), int(32 * s), int(20 * s), int(50 * s), GOLD),      # thân vàng
        (int(27.5 * s), int(22 * s), int(36.5 * s), int(50 * s), GREEN), # thân xanh
        (int(44 * s), int(12 * s), int(53 * s), int(50 * s), GOLD),      # thân vàng
    ]
    for x1, y1, x2, y2, c in bars:
        d.rounded_rectangle([x1, y1, x2, y2], radius=int(2.5 * s), fill=c)
    return img


# 1) Icon app iOS 1024x1024 (App Store yêu cầu vuông, không trong suốt, KHÔNG bo góc sẵn — iOS tự bo)
icon = candle_logo(1024, rounded=False)
icon_path = os.path.join(ASSETS, "AppIcon.appiconset", "AppIcon1024.png")
icon.convert("RGB").save(icon_path, "PNG")
print("OK  ->", icon_path)

# 2) Logo launch screen (nền trong suốt, chỉ 3 nến)
logo = candle_logo(192, rounded=False)
# bỏ nền để launch screen trong suốt trên màu LaunchBackground
px = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        if px[x, y][:3] == BG:
            px[x, y] = (0, 0, 0, 0)
logo_path = os.path.join(ASSETS, "LaunchLogo.imageset", "launch-logo.png")
logo.save(logo_path, "PNG")
print("OK  ->", logo_path)

# 3) Icon web cho PWA: 192 + 512 (bo góc mềm) + apple-touch-icon 180 (iOS cắt vuông, nên bo sẵn)
for name, size, rounded in [("icon-192.png", 192, True), ("icon-512.png", 512, True), ("apple-touch-icon.png", 180, True)]:
    img = candle_logo(size, rounded=rounded)
    if name == "apple-touch-icon.png":
        img = img.convert("RGB")  # iOS không render alpha tốt trên apple-touch-icon — thay nền đen
    out = os.path.join(ROOT, name)
    img.save(out, "PNG")
    print("OK  ->", out)
