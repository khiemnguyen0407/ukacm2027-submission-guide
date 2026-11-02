"""Small toolkit to clean up and annotate CMT screenshots (Pillow only).

All coordinates passed to the drawing helpers are in ORIGINAL screenshot pixels
(after cropping). The figure is rendered at SCALE x for crisp annotations.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw")
OUT = os.path.join(HERE, "..")
SCALE = 2

ORANGE = (217, 115, 26)
ORANGE_PALE = (255, 244, 224)
RED = (192, 57, 43)
RED_PALE = (253, 236, 234)
INK = (30, 39, 51)
GREY = (91, 102, 117)
BORDER = (197, 205, 216)

_F = {
    "ui": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "ui-b": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "ann": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "ann-b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}


def font(kind, size):
    return ImageFont.truetype(_F[kind], int(round(size * SCALE)))


def load(name):
    return Image.open(os.path.join(RAW, name)).convert("RGB")


def vstack(parts, gap=0, bg=(255, 255, 255)):
    w = max(p.width for p in parts)
    h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    out = Image.new("RGB", (w, h), bg)
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height + gap
    return out


def hstack(parts, gap=0, bg=(255, 255, 255)):
    h = max(p.height for p in parts)
    w = sum(p.width for p in parts) + gap * (len(parts) - 1)
    out = Image.new("RGB", (w, h), bg)
    x = 0
    for p in parts:
        out.paste(p, (x, 0))
        x += p.width + gap
    return out


def replace_text(im, box, text, size=16, color=(51, 51, 51), bg=None, bold=False, dx=0):
    """Paint over box (orig px, before scaling) and write replacement text (used to anonymise)."""
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    if bg is None:
        bg = im.getpixel((x0, y0))
    d.rectangle(box, fill=bg)
    f = ImageFont.truetype(_F["ui-b" if bold else "ui"], size)
    d.text((x0 + dx, (y0 + y1) / 2), text, font=f, fill=color, anchor="lm")


def erase(im, box, bg=None):
    d = ImageDraw.Draw(im)
    if bg is None:
        bg = im.getpixel((box[0], box[1]))
    d.rectangle(box, fill=bg)


class Fig:
    """Screenshot placed on a canvas with margins for callouts, plus border & shadow."""

    def __init__(self, shot, margin=(18, 18, 18, 18)):
        l, t, r, b = margin
        self.ox, self.oy = l, t
        self.shot = shot
        W = (shot.width + l + r) * SCALE
        H = (shot.height + t + b) * SCALE
        self.im = Image.new("RGB", (W, H), (255, 255, 255))
        # soft shadow
        sh = Image.new("L", (W, H), 0)
        ds = ImageDraw.Draw(sh)
        x0, y0 = (l + 3) * SCALE, (t + 5) * SCALE
        ds.rounded_rectangle([x0, y0, x0 + shot.width * SCALE, y0 + shot.height * SCALE],
                             radius=10 * SCALE, fill=90)
        sh = sh.filter(ImageFilter.GaussianBlur(7 * SCALE))
        self.im.paste((150, 160, 175), (0, 0), sh)
        big = shot.resize((shot.width * SCALE, shot.height * SCALE), Image.LANCZOS)
        mask = Image.new("L", big.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, big.width - 1, big.height - 1],
                                               radius=8 * SCALE, fill=255)
        self.im.paste(big, (l * SCALE, t * SCALE), mask)
        self.d = ImageDraw.Draw(self.im)
        self.d.rounded_rectangle([l * SCALE, t * SCALE, (l + shot.width) * SCALE - 1,
                                  (t + shot.height) * SCALE - 1], radius=8 * SCALE,
                                 outline=BORDER, width=2 * SCALE // 2 + 1)

    # coordinate helpers (orig screenshot px -> canvas px)
    def P(self, x, y):
        return ((self.ox + x) * SCALE, (self.oy + y) * SCALE)

    def B(self, box, pad=0):
        x0, y0, x1, y1 = box
        a = self.P(x0 - pad, y0 - pad)
        b = self.P(x1 + pad, y1 + pad)
        return [a[0], a[1], b[0], b[1]]

    def box(self, box, color=ORANGE, width=3, pad=4, radius=6, fill=None):
        self.d.rounded_rectangle(self.B(box, pad), radius=radius * SCALE,
                                 outline=color, width=width * SCALE, fill=fill)

    def badge(self, x, y, n, color=ORANGE, r=16):
        cx, cy = self.P(x, y)
        R = r * SCALE
        self.d.ellipse([cx - R - 3 * SCALE, cy - R - 3 * SCALE, cx + R + 3 * SCALE, cy + R + 3 * SCALE],
                       fill=(255, 255, 255))
        self.d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=color)
        self.d.text((cx, cy + 1), str(n), font=font("ann-b", 17), fill=(255, 255, 255), anchor="mm")

    def line(self, pts, color=ORANGE, width=2, dot=True):
        P = [self.P(*p) for p in pts]
        self.d.line(P, fill=color, width=width * SCALE, joint="curve")
        if dot:
            x, y = P[-1]
            r = 4 * SCALE
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def label(self, x, y, text, color=ORANGE, fill=ORANGE_PALE, size=16, anchor="l",
              n=None, bold_first=False, width=None):
        """Callout box. (x, y) is the left-middle (anchor 'l') or right-middle ('r') point."""
        f = font("ann", size)
        fb = font("ann-b", size)
        lines = text.split("\n")
        lh = int(size * 1.35 * SCALE)
        tw = max(self.d.textlength(ln, font=(fb if (bold_first and i == 0) else f))
                 for i, ln in enumerate(lines))
        padx, pady = 10 * SCALE, 7 * SCALE
        bw = int(width * SCALE) if width else int(tw + 2 * padx + (34 * SCALE if n is not None else 0))
        bh = lh * len(lines) + 2 * pady
        px, py = self.P(x, y)
        x0 = px if anchor == "l" else px - bw
        y0 = py - bh // 2
        self.d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=7 * SCALE, fill=fill,
                                 outline=color, width=2 * SCALE)
        tx = x0 + padx
        if n is not None:
            R = 13 * SCALE
            cx, cy = x0 + padx + R, y0 + bh // 2
            self.d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=color)
            self.d.text((cx, cy + 1), str(n), font=font("ann-b", 14), fill=(255, 255, 255), anchor="mm")
            tx += 2 * R + 8 * SCALE
        for i, ln in enumerate(lines):
            self.d.text((tx, y0 + pady + i * lh + lh // 2), ln,
                        font=(fb if (bold_first and i == 0) else f), fill=INK, anchor="lm")
        # return box in orig coords for leader lines
        return ((x0 / SCALE) - self.ox, (y0 / SCALE) - self.oy,
                ((x0 + bw) / SCALE) - self.ox, ((y0 + bh) / SCALE) - self.oy)

    def break_mark(self, x, y0, y1):
        """Zig-zag 'content omitted' marker drawn vertically at x (orig px)."""
        pts, up = [], True
        y = y0
        while y <= y1:
            pts.append((x + (5 if up else -5), y))
            up = not up
            y += 8
        self.line(pts, color=GREY, width=2, dot=False)

    def save(self, name):
        path = os.path.join(OUT, name)
        self.im.save(path, optimize=True)
        return path
