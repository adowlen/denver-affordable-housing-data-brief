"""Composite the headline figure over the generated hero illustration."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

PKG = pathlib.Path(__file__).resolve().parent.parent
src = next((PKG / "hero_source").glob("media-generation-hero-illustration-*.webp"))
img = Image.open(src).convert("RGB")
W, H = img.size
d = ImageDraw.Draw(img, "RGBA")
# gradient scrim over the top field
for y in range(int(H * 0.42)):
    a = int(200 * (1 - y / (H * 0.42)))
    d.line([(0, y), (W, y)], fill=(16, 16, 16, a))
def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)
d.text((60, 55), "29,474", font=font(150), fill=(242, 169, 0))
d.text((62, 225), "income-restricted homes in Denver", font=font(58), fill=(232, 232, 232))
d.text((62, 300), "15 of 78 neighborhoods: none listed", font=font(58), fill=(42, 200, 180))
d.text((62, 385), "Source: Denver HOST Affordable Housing Inventory, pulled Oct 21, 2026", font=font(30, bold=False), fill=(200, 200, 200))
img.save(PKG / "hero.png")
print("hero.png", img.size)
