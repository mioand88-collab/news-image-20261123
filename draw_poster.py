"""Draw the 23 November 2026 front-page poster (1024x1024 PNG).

All artwork is drawn from scratch with PIL: shapes, gradients and
typography only. No photos, no downloaded images.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=4):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def main():
    img = Image.new("RGB", (W, H), (250, 246, 238))
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 8], fill=(178, 34, 34))
    d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SERIF, 62),
           fill=(20, 20, 20), anchor="ma")
    d.text((512, 96), "MONDAY 23 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE IMAGE",
           font=font(SANS_BOLD, 21), fill=(178, 34, 34), anchor="ma")
    d.line([36, 128, 988, 128], fill=(20, 20, 20), width=3)
    d.line([36, 134, 988, 134], fill=(20, 20, 20), width=1)

    # --- LEAD: COP31 collapse ---
    d.rectangle([36, 148, 988, 470], fill=(16, 58, 66))
    # drawn scene: hazy sun over smokestacks
    d.ellipse([700, 180, 900, 380], fill=(232, 160, 60))
    d.ellipse([730, 210, 870, 350], fill=(244, 196, 110))
    for i, x in enumerate((640, 730, 820)):
        d.rectangle([x, 300 + i * 12, x + 52, 470], fill=(10, 38, 44))
        d.rectangle([x + 8, 282 + i * 12, x + 44, 302 + i * 12], fill=(10, 38, 44))
    d.rectangle([36, 430, 988, 470], fill=(10, 38, 44))
    d.text((64, 168), "CLIMATE", font=font(SERIF, 26), fill=(232, 160, 60))
    y = text_block(d, 64, 200, "COP31 talks collapse",
                   font(SERIF, 46), (250, 246, 238), 560, leading=2)
    y = text_block(d, 64, y + 4, "with no deal agreed",
                   font(SERIF, 46), (250, 246, 238), 560, leading=2)
    text_block(d, 64, y + 12,
               "Nations in Antalya fail to agree a pact as the final "
               "draft drops any mention of fossil fuels. The EU and "
               "others reject it; talks end without agreement.",
               font(SANS, 21), (220, 228, 226), 560, leading=5)

    # --- row 2: two stories ---
    # Iran / Hormuz (left)
    d.rectangle([36, 490, 500, 700], fill=(255, 255, 255),
                outline=(20, 20, 20), width=2)
    d.rectangle([36, 490, 500, 530], fill=(178, 34, 34))
    d.text((52, 496), "MIDDLE EAST", font=font(SANS_BOLD, 19), fill=(255, 255, 255))
    y = text_block(d, 52, 544, "Iran strikes US bases in Bahrain",
                   font(SERIF, 34), (20, 20, 20), 420, leading=2)
    text_block(d, 52, y + 8,
               "Missiles hit US military sites as the Strait of Hormuz "
               "crisis deepens; Bahrain says attacks were repelled.",
               font(SANS, 20), (40, 40, 40), 420, leading=4)
    # Ukraine (right)
    d.rectangle([524, 490, 988, 700], fill=(255, 255, 255),
                outline=(20, 20, 20), width=2)
    d.rectangle([524, 490, 988, 530], fill=(30, 70, 140))
    d.text((540, 496), "UKRAINE", font=font(SANS_BOLD, 19), fill=(255, 255, 255))
    y = text_block(d, 540, 544, "Drone strike hits Kyiv region",
                   font(SERIF, 34), (20, 20, 20), 420, leading=2)
    text_block(d, 540, y + 8,
               "At least 14 people missing after a Russian drone hits "
               "a building; a supermarket strike kills three.",
               font(SANS, 20), (40, 40, 40), 420, leading=4)

    # --- row 3: three stories ---
    panels = [
        (36, "MEXICO", "Cartel boss captured",
         "Mexico seizes FBI most-wanted 'El Chapo Isidro' after "
         "firefights in Sinaloa leave 11 dead."),
        (356, "ASIA", "Nepal PM meets Modi",
         "Nepal's Balendra Shah holds talks with India's PM in "
         "New Delhi on his state visit."),
        (676, "SPORT", "India's record 720/9",
         "India post a record 720 for 9 declared in the Wellington "
         "Test against New Zealand."),
    ]
    for x, tag, head, body in panels:
        d.rectangle([x, 720, x + 296, 920], fill=(255, 255, 255),
                    outline=(20, 20, 20), width=2)
        d.rectangle([x, 720, x + 296, 754], fill=(20, 20, 20))
        d.text((x + 14, 726), tag, font=font(SANS_BOLD, 18), fill=(255, 255, 255))
        y = text_block(d, x + 14, 766, head, font(SERIF, 27),
                       (20, 20, 20), 268, leading=2)
        text_block(d, x + 14, y + 8, body, font(SANS, 18),
                   (40, 40, 40), 268, leading=4)

    # --- footer strip: also today ---
    d.rectangle([36, 940, 988, 996], fill=(20, 20, 20))
    text_block(d, 52, 950,
               "ALSO TODAY: South Korea's education minister quits over an "
               "AI exam-cheating scandal  •  Indonesia factory fire: "
               "dozens missing  •  Russian cargo ship still burning off Finland",
               font(SANS_BOLD, 17), (250, 246, 238), 920, leading=3)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
