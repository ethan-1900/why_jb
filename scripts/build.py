"""从原始 Markdown 生成博客，并生成不覆盖原图的网页优化图片。"""
from pathlib import Path
import re
import shutil
import markdown
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent


def check_font_subset(text):
    """正文改字后，提醒重新生成自托管的思源宋体子集。

    子集只收录生成当时出现过的字符，缺字会静默回退到系统字体，和上下文出现字形差异。
    """
    subset = ROOT / 'assets' / 'source-han-serif-sc-subset.woff2'
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return
    if not subset.exists():
        return
    plain = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', text)
    covered = set(TTFont(subset).getBestCmap())
    missing = sorted({ch for ch in plain if not ch.isspace() and ord(ch) not in covered})
    if missing:
        print(f'⚠️  字体子集缺少 {len(missing)} 个字符：{"".join(missing)}')
        print('    请执行 python3 scripts/subset_font.py 重新生成，否则这些字会回退到系统字体。')


source = (ROOT / 'Why JB.md').read_text()
check_font_subset(source)
content = re.sub(r'^# Why JB[^\n]*\n', '', source, count=1).lstrip()
content = re.sub(r'==(.+?)==', r'<mark>\1</mark>', content)
body = markdown.markdown(content, extensions=['extra', 'sane_lists'])
body = re.sub(r'<img ', '<img loading="lazy" decoding="async" ', body)

# 竖图、方图用 compact-image 缩小展示；横图不缩，统一铺到正文 90% 宽，边缘彼此对齐。
for filename in dict.fromkeys(re.findall(r'Attachments/([^\s)]+\.jpeg)', source)):
    original = ROOT / 'Attachments' / filename
    with Image.open(original) as image:
        width, height = ImageOps.exif_transpose(image).size
    if width / height <= 1.15:
        src = f'src="Attachments/{filename}"'
        body = body.replace(src, f'class="compact-image" {src}')

optimized_dir = ROOT / 'assets' / 'optimized'
optimized_dir.mkdir(parents=True, exist_ok=True)
image_refs = dict.fromkeys(re.findall(r'Attachments/([^\s)]+\.jpeg)', source))
for filename in image_refs:
    original = ROOT / 'Attachments' / filename
    optimized = optimized_dir / f'{original.stem}.webp'
    with Image.open(original) as image:
        image = ImageOps.exif_transpose(image).convert('RGB')
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        image.save(optimized, 'WEBP', quality=82, method=6)

def use_optimized_image(match):
    tag = match.group(0)
    filename = match.group(1)
    webp = f'assets/optimized/{Path(filename).stem}.webp'
    return f'<picture><source srcset="{webp}" type="image/webp">{tag}</picture>'

body = re.sub(
    r'<img\b[^>]*\bsrc="Attachments/([^"/]+\.jpeg)"[^>]*>',
    use_optimized_image,
    body,
)
template = (ROOT / 'template.html').read_text()
page = template.replace('{{ARTICLE}}', body)
out = ROOT / '_site'
out.mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(page)
shutil.copy2(out / 'index.html', ROOT / 'index.html')  # 仓库根目录才是 GitHub Pages 的发布目录
shutil.copy2(ROOT / 'Why JB.md', out / 'Why JB.md')
shutil.copytree(ROOT / 'Attachments', out / 'Attachments', dirs_exist_ok=True, ignore=shutil.ignore_patterns('.DS_Store'))
shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
(out / '.nojekyll').touch()
print(f'已生成 {out / "index.html"}')
