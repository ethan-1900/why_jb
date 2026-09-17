#!/usr/bin/env python3
"""重建正文衬线字体子集（assets/source-han-serif-sc-subset.woff2）。

正文排版用的是自托管的思源宋体子集：只收录生成当时文章里出现过的字符。
因此**每次改动 Why JB.md 的文字之后**都要重新执行本脚本，否则新字不在子集里，
浏览器会回退到系统字体，和上下文出现字形 / 字重差异（例如「打」曾缺失，
在没装思源宋体的机器上会掉到 Songti SC）。

用法：
    python3 scripts/subset_font.py           # 重新生成子集
    python3 scripts/subset_font.py --check   # 只报告覆盖情况，不写文件
"""
from pathlib import Path
import re
import sys

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE_CANDIDATES = [
    Path.home() / 'Library/Fonts/SourceHanSerifSC-Regular.otf',
    Path('/Library/Fonts/SourceHanSerifSC-Regular.otf'),
    Path.home() / 'Library/Fonts/SourceHanSerifSC-Regular.ttf',
]
TARGET = ROOT / 'assets' / 'source-han-serif-sc-subset.woff2'

# 文章之外的常见中文标点与符号，留一点余量，顺手收录。
EXTRA_CHARS = '、。，．；：？！…—～·《》〈〉「」『』（）【】〔〕“”‘’'


def article_text() -> str:
    """取出正文的可见字符（去掉 Markdown 图片语法与代码标记）。"""
    md = (ROOT / 'Why JB.md').read_text(encoding='utf-8')
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', md)
    return md + EXTRA_CHARS


def wanted_chars() -> set[str]:
    return {ch for ch in article_text() if not ch.isspace()}


def target_coverage() -> tuple[set[int], set[str]]:
    covered = set(TTFont(TARGET).getBestCmap())
    missing = {ch for ch in wanted_chars() if ord(ch) not in covered}
    return covered, missing


def subset(source: Path) -> None:
    options = Options()
    options.flavor = 'woff2'
    options.desubroutinize = True
    options.recalc_bounds = True
    font = TTFont(source)
    subsetter = Subsetter(options=options)
    subsetter.populate(text=''.join(sorted(wanted_chars())))
    subsetter.subset(font)
    font.flavor = 'woff2'
    font.save(TARGET)


def main() -> int:
    if '--check' in sys.argv:
        covered, missing = target_coverage()
        print(f'子集覆盖 {len(covered)} 个码位；文章需要 {len(wanted_chars())} 个字符')
        print('缺失：' + (''.join(sorted(missing)) if missing else '（无）'))
        return 1 if missing else 0

    source = next((p for p in SOURCE_CANDIDATES if p.exists()), None)
    if source is None:
        print('找不到思源宋体源文件，请先安装 Source Han Serif SC Regular：')
        for path in SOURCE_CANDIDATES:
            print(f'  - {path}')
        return 2

    before = TARGET.stat().st_size if TARGET.exists() else 0
    subset(source)
    covered, missing = target_coverage()
    after = TARGET.stat().st_size
    print(f'源字体：{source}')
    print(f'已写出 {TARGET.relative_to(ROOT)}（{before / 1024:.0f} KB → {after / 1024:.0f} KB，{len(covered)} 个码位）')
    print('缺失：' + (''.join(sorted(missing)) if missing else '（无）'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
