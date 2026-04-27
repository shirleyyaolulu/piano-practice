#!/usr/bin/env python3
"""
Generate a Xiaohongshu cover image — 手写笔记风格（精简版）
大标题 + 副标题 + 几句卖点，留白干净
"""

from PIL import Image, ImageDraw, ImageFont
import random, os, math

W, H = 1080, 1440
random.seed(42)

# ── Fonts ──
serif_bold = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
sans_regular = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
sans_medium = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
sans_bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

f_title   = ImageFont.truetype(serif_bold, 92)
f_sub     = ImageFont.truetype(serif_bold, 56)
f_body    = ImageFont.truetype(sans_medium, 38)
f_label   = ImageFont.truetype(sans_bold, 30)
f_small   = ImageFont.truetype(sans_regular, 28)
f_tiny    = ImageFont.truetype(sans_regular, 24)

# ── Colors ──
PAPER     = (252, 249, 242)
INK       = (45, 40, 38)
INK_LIGHT = (120, 110, 105)
RED_PEN   = (200, 60, 55)
BLUE_PEN  = (55, 90, 160)
PENCIL    = (160, 150, 135)
YELLOW_HL = (255, 245, 140, 90)
LINE_GRAY = (215, 210, 200)

# ── Background: 纸张质感 ──
img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# 纸张纹理：随机浅色噪点
for _ in range(8000):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    v = random.randint(240, 255)
    img.putpixel((x, y), (v, v - random.randint(0, 5), v - random.randint(0, 8)))

# 左侧红色竖线（笔记本风格）
draw.line([(100, 0), (100, H)], fill=(220, 180, 175), width=2)
draw.line([(104, 0), (104, H)], fill=(220, 180, 175), width=2)

# 横格线
for y in range(180, H, 65):
    draw.line([(0, y), (W, y)], fill=LINE_GRAY, width=1)

# ── 右上角红色标签 ──
draw.rounded_rectangle([(800, 60), (1020, 108)], radius=8, fill=RED_PEN)
draw.text((825, 68), "亲测 11 周", fill=(255, 255, 255), font=f_label)

# ── 大标题 ── 视觉重心在上半部分
# 黄色高亮效果
hl_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hl_draw = ImageDraw.Draw(hl_img)
hl_draw.rectangle([(110, 220), (920, 330)], fill=YELLOW_HL)
hl_draw.rectangle([(110, 350), (790, 460)], fill=YELLOW_HL)
img.paste(Image.alpha_composite(
    Image.new("RGBA", (W, H), (*PAPER, 255)), hl_img
).convert("RGB"))
draw = ImageDraw.Draw(img)

# 重绘标签（被高亮层覆盖了需要重画）
draw.rounded_rectangle([(800, 60), (1020, 108)], radius=8, fill=RED_PEN)
draw.text((825, 68), "亲测 11 周", fill=(255, 255, 255), font=f_label)

draw.text((120, 210), "不懂钢琴的家长", fill=INK, font=f_title)
draw.text((120, 345), "怎么陪娃练琴？", fill=INK, font=f_title)

# ── 副标题 ──
draw.text((120, 500), "——让 AI 帮你做每周练习计划", fill=BLUE_PEN, font=f_sub)

# ── 分隔波浪线 ──
wave_y = 590
for x in range(120, 960, 4):
    dy = int(3 * math.sin(x * 0.05))
    draw.ellipse([(x, wave_y + dy), (x + 2, wave_y + dy + 2)], fill=PENCIL)

# ── 核心卖点 ──
y = 650
bullets = [
    "· 每天20分钟，照着做就行",
    "· 新曲旧曲，AI帮你安排",
    "· 家长完全不需要懂钢琴",
]
for text in bullets:
    draw.text((140, y), text, fill=INK, font=f_body)
    y += 62

# ── 结果金句 ──
y += 35

# 手绘下划线
for x in range(120, 960, 4):
    dy = int(2 * math.sin(x * 0.06 + 1))
    draw.ellipse([(x, y + dy), (x + 2, y + dy + 2)], fill=PENCIL)

y += 22
draw.text((120, y), "11周：食指点琴 → 三指弹15首曲子", fill=RED_PEN, font=f_body)

y += 58
draw.text((120, y), "老师问我在家怎么练的", fill=INK_LIGHT, font=f_body)

# ── 底部标签 ──
draw.text((120, H - 90), "#钢琴启蒙  #AI陪练  #琴童妈妈", fill=PENCIL, font=f_tiny)

# ── 保存 ──
output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xhs_cover.png")
img.save(output, "PNG", quality=95)
print(f"Saved to {output}")
