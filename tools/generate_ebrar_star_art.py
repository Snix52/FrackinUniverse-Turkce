"""Draw the original Ebrar's Star lamp with the Python standard library.

Run this file to regenerate all PNGs. Each image uses a 16 x 16 Starbound
pixel grid; enlarge with nearest-neighbor sampling only.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


OUT = Path(__file__).resolve().parent / 'custom_assets/objects/decorative/futrebrarstar'
SIZE = 16
TRANSPARENT = (0, 0, 0, 0)

PALETTE = {
    "shadow": (17, 25, 48, 210),
    "rim": (42, 51, 79, 255),
    "bronze": (140, 86, 61, 255),
    "gold": (239, 166, 72, 255),
    "cream": (255, 228, 157, 255),
    "white": (255, 250, 215, 255),
    "rose_dark": (138, 60, 101, 255),
    "rose": (242, 103, 146, 255),
    "rose_light": (255, 170, 187, 255),
    "glow_gold": (255, 206, 99, 75),
    "glow_rose": (255, 128, 162, 72),
}


def canvas(width: int = SIZE, height: int = SIZE):
    return [[TRANSPARENT for _ in range(width)] for _ in range(height)]


def set_px(pixels, x: int, y: int, color):
    if 0 <= x < len(pixels[0]) and 0 <= y < len(pixels):
        pixels[y][x] = color


def point_inside(px: float, py: float, vertices) -> bool:
    inside = False
    last_x, last_y = vertices[-1]
    for x, y in vertices:
        if (y > py) != (last_y > py):
            cross_x = (last_x - x) * (py - y) / (last_y - y) + x
            if px < cross_x:
                inside = not inside
        last_x, last_y = x, y
    return inside


def star_mask():
    # Five-point silhouette with short arms so it reads at game scale.
    vertices = [
        (7.5, 0.0), (10.0, 5.0), (15.3, 5.2), (11.0, 9.0),
        (12.8, 15.2), (7.5, 11.4), (2.2, 15.2), (4.0, 9.0),
        (-0.3, 5.2), (5.0, 5.0),
    ]
    return [[point_inside(x + 0.5, y + 0.5, vertices)
             for x in range(SIZE)] for y in range(SIZE)]


def draw_lamp(lit: bool):
    pixels = canvas()
    mask = star_mask()

    # One-pixel offset gives a restrained dark mount and a clear outline.
    for y in range(SIZE):
        for x in range(SIZE):
            if mask[y][x]:
                set_px(pixels, x, y, PALETTE["rim"])
                if x + 1 < SIZE and y + 1 < SIZE:
                    set_px(pixels, x + 1, y + 1, PALETTE["shadow"])

    for y in range(SIZE):
        for x in range(SIZE):
            if not mask[y][x]:
                continue
            edge = any(
                not (0 <= x + dx < SIZE and 0 <= y + dy < SIZE
                     and mask[y + dy][x + dx])
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
            )
            if edge:
                color = PALETTE["bronze"]
            elif y < 7 or x < 6:
                color = PALETTE["gold"]
            else:
                color = PALETTE["cream"]
            set_px(pixels, x, y, color)

    # Six asymmetric highlights keep the metal from looking flat.
    for x, y in ((7, 2), (8, 2), (2, 6), (5, 6), (10, 6), (4, 11)):
        if mask[y][x]:
            set_px(pixels, x, y, PALETTE["white"] if lit else PALETTE["cream"])

    # Tiny heart in the jewel; no lettering that becomes illegible at 1x.
    heart = {
        (6, 7): "rose_dark", (7, 7): "rose", (8, 7): "rose_dark",
        (9, 7): "rose_light", (6, 8): "rose", (7, 8): "rose_light",
        (8, 8): "rose_light", (9, 8): "rose", (7, 9): "rose",
        (8, 9): "rose", (8, 10): "rose_dark",
    }
    for (x, y), color in heart.items():
        set_px(pixels, x, y, PALETTE[color])

    return pixels


def draw_fullbright():
    pixels = canvas()
    mask = star_mask()
    for y in range(SIZE):
        for x in range(SIZE):
            if mask[y][x]:
                pixels[y][x] = PALETTE["cream"]
            elif any(0 <= x + dx < SIZE and 0 <= y + dy < SIZE
                     and mask[y + dy][x + dx]
                     for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                pixels[y][x] = PALETTE["glow_gold"]
    for x, y in ((7, 1), (8, 1), (2, 6), (13, 6), (6, 12), (9, 12)):
        set_px(pixels, x, y, PALETTE["white"])
    for y in (7, 8):
        for x in (7, 8):
            set_px(pixels, x, y, PALETTE["rose_light"])
    return pixels


def chunk(kind: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def write_png(path: Path, pixels):
    width, height = len(pixels[0]), len(pixels)
    payload = b"".join(b"\x00" + b"".join(bytes(px) for px in row)
                       for row in pixels)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(payload, 9))
           + chunk(b"IEND", b""))
    path.write_bytes(png)


def preview(off, on):
    scale = 12
    width, height = 2 * 16 * scale + 3 * 24, 16 * scale + 48
    dark = (22, 32, 61, 255)
    darker = (17, 24, 44, 255)
    pixels = [[dark if ((x // 24 + y // 24) % 2 == 0) else darker
               for x in range(width)] for y in range(height)]
    for image, start_x in ((off, 24), (on, 2 * 24 + 16 * scale)):
        for sy, row in enumerate(image):
            for sx, px in enumerate(row):
                if px[3] == 0:
                    continue
                for yy in range(24 + sy * scale, 24 + (sy + 1) * scale):
                    for xx in range(start_x + sx * scale,
                                    start_x + (sx + 1) * scale):
                        pixels[yy][xx] = px
    return pixels


def main():
    off = draw_lamp(False)
    on = draw_lamp(True)
    write_png(OUT / "ebrarstar.png", off)
    write_png(OUT / "ebrarstaricon.png", on)
    write_png(OUT / "ebrarstarlit.png", draw_fullbright())


if __name__ == "__main__":
    main()
