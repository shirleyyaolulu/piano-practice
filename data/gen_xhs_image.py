#!/usr/bin/env python3
"""
Generate a Xiaohongshu cover image — 手写笔记风格
模拟：浅色纸张背景 + 手写风大标题 + 简洁内容，像家长自己写的笔记
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os, math

W, H = 1080, 1440
random.seed(42)

# ── Fonts ──
serif_bold = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
sans_regular = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
sans_medium = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
sans_bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

f_title   = ImageFont.truetype(serif_bold, 72)
f_title_s = ImageFont.truetype(serif_bold, 50)
f_body    = ImageFont.truetype(sans_regular, 33)
f_body_m  = ImageFont.truetype(sans_medium, 33)
f_label   = ImageFont.truetype(sans_bold, 27)
f_day     = ImageFont.truetype(sans_bold, 30)
f_small   = ImageFont.truetype(sans_regular, 26)
f_tiny    = ImageFont.truetype(sans_regular, 22)

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
for y in range(180, H, 60):
    draw.line([(0, y), (W, y)], fill=LINE_GRAY, width=1)

# ── 顶部日期区域 ──
draw.text((130, 40), "2026 / 4 / 27  Sun", fill=PENCIL, font=f_small)
draw.text((130, 72), "Week 11 练琴笔记", fill=PENCIL, font=f_small)

# 右上角小标签
draw.rounded_rectangle([(830, 35), (1040, 80)], radius=8, fill=RED_PEN)
draw.text((855, 42), "亲测 11 周", fill=(255, 255, 255), font=f_label)

# ── 标题区 ──
# 黄色高亮效果
hl_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hl_draw = ImageDraw.Draw(hl_img)
hl_draw.rectangle([(120, 170), (870, 252)], fill=YELLOW_HL)
hl_draw.rectangle([(120, 262), (720, 344)], fill=YELLOW_HL)
img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (*PAPER, 255)), hl_img).convert("RGB"))

draw = ImageDraw.Draw(img)

draw.text((130, 165), "不懂钢琴的家长", fill=INK, font=f_title)
draw.text((130, 260), "怎么陪娃练琴？", fill=INK, font=f_title)

# 副标题
draw.text((130, 370), "——让 AI 帮你做每周练习计划", fill=BLUE_PEN, font=f_title_s)

# ── 分隔：手绘波浪线 ──
wave_y = 445
for x in range(130, 950, 4):
    dy = int(3 * math.sin(x * 0.05))
    draw.ellipse([(x, wave_y + dy), (x + 2, wave_y + dy + 2)], fill=PENCIL)

# ── 痛点区域 ──
y = 475
draw.text((130, y), "以前的我：", fill=RED_PEN, font=f_body_m)
y += 48

pains = [
    "不知道今天该练什么",
    "练了新曲 旧曲全忘",
    "孩子说不练就干瞪眼",
    "自己五线谱都看不懂",
]
for pain in pains:
    draw.text((145, y - 2), "x", fill=RED_PEN, font=f_body_m)
    draw.text((185, y), pain, fill=INK, font=f_body)
    bbox = draw.textbbox((185, y), pain, font=f_body)
    mid_y = (bbox[1] + bbox[3]) // 2
    draw.line([(185, mid_y), (bbox[2], mid_y)], fill=RED_PEN, width=2)
    y += 42

# ── 解法区域 ──
y += 10
draw.text((130, y), "现在的做法：", fill=BLUE_PEN, font=f_body_m)

box_top = y + 42
box_bottom = box_top + 170
draw.rounded_rectangle([(125, box_top), (960, box_bottom)], radius=12,
                       outline=BLUE_PEN, width=2)

y = box_top + 12
steps = [
    "1. 上完课 → 告诉AI今天学了啥",
    "2. AI生成一周6天练琴计划",
    "3. 每晚照着带娃做 20分钟",
]
for step in steps:
    draw.text((155, y), step, fill=INK, font=f_body_m)
    y += 50

# ── 一周安排示意 ──
y = box_bottom + 18
draw.text((130, y), "一周长这样:", fill=INK_LIGHT, font=f_body_m)
y += 40

days = [
    ("周一", "巩固日", "趁热复习课堂内容"),
    ("周二", "轻松日", "10分钟小游戏就够"),
    ("周三", "主练日", "重点突破这周难点"),
    ("周四", "游戏日", "抽号弹旧曲 超好玩"),
    ("周五", "冒险日", "编故事串着练"),
    ("周六", "展示日", "课前回顾 给自己打分"),
]

colors_day = [BLUE_PEN, (100, 160, 120), BLUE_PEN, (190, 120, 50), RED_PEN, (100, 160, 120)]

for i, (day_name, day_type, desc) in enumerate(days):
    color = colors_day[i]
    draw.text((145, y), day_name, fill=color, font=f_day)
    draw.rounded_rectangle([(230, y + 2), (348, y + 36)], radius=6, fill=color)
    bbox_t = draw.textbbox((0, 0), day_type, font=f_label)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((230 + (118 - tw) // 2, y + 5), day_type, fill=(255, 255, 255), font=f_label)
    draw.text((365, y + 4), desc, fill=INK_LIGHT, font=f_small)
    y += 42

# ── 底部重点 ──
y += 14

# 手绘下划线
for x in range(130, 950, 4):
    dy = int(2 * math.sin(x * 0.06 + 1))
    draw.ellipse([(x, y + dy), (x + 2, y + dy + 2)], fill=PENCIL)

y += 14
draw.text((130, y), "关键是：", fill=INK, font=f_body_m)
draw.text((295, y), "家长完全不需要懂钢琴", fill=RED_PEN, font=f_body_m)

y += 44
draw.text((130, y), "AI会告诉你该说什么、该做什么、该夸什么", fill=INK, font=f_body)

y += 46
draw.text((130, y), "11周下来，从食指点琴 → 三指弹15首曲子", fill=BLUE_PEN, font=f_body_m)

y += 44
draw.text((130, y), "老师问我在家怎么练的", fill=INK_LIGHT, font=f_body)

# ── 右下角小装饰 ──
draw.text((820, H - 80), "# 钢琴启蒙", fill=PENCIL, font=f_tiny)
draw.text((820, H - 50), "# AI陪练", fill=PENCIL, font=f_tiny)

# ── 保存 ──
output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xhs_cover.png")
img.save(output, "PNG", quality=95)
print(f"Saved to {output}")
