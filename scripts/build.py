"""从原始 Markdown 生成博客；不修改文章或图片。"""
from pathlib import Path
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parent.parent
source = (ROOT / 'Why JB.md').read_text()
content = re.sub(r'^# Why JB[^\n]*\n', '', source, count=1).lstrip()
content = re.sub(r'==(.+?)==', r'<mark>\1</mark>', content)
body = markdown.markdown(content, extensions=['extra', 'sane_lists'])
body = re.sub(r'<img ', '<img loading="lazy" decoding="async" ', body)
body = body.replace(
    'src="Attachments/A82392B5-4DCA-4606-B153-D2C94CF879E4.jpeg"',
    'class="compact-image" src="Attachments/A82392B5-4DCA-4606-B153-D2C94CF879E4.jpeg"',
)
template = (ROOT / 'template.html').read_text()
page = template.replace('{{ARTICLE}}', body)
out = ROOT / '_site'
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(page)
shutil.copy2(ROOT / 'Why JB.md', out / 'Why JB.md')
shutil.copytree(ROOT / 'Attachments', out / 'Attachments', dirs_exist_ok=True, ignore=shutil.ignore_patterns('.DS_Store'))
shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
(out / '.nojekyll').touch()
print(f'已生成 {out / "index.html"}')
