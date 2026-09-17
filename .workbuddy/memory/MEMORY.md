# Why JB 项目约定

## 结构

- `Why JB.md` 是唯一内容源，图片放 `Attachments/`，正文用相对路径引用。
- `template.html` 是页面模板（含内联样式与脚本），`{{ARTICLE}}` 由构建脚本替换。
- `assets/style.css` 是共享样式（构建不压缩、原样拷贝）。
- `scripts/build.py` 生成 `_site/`，**并把 `_site/index.html` 复制到仓库根目录**——
  根目录 `index.html` 才是 GitHub Pages 实际发布的入口（Pages 从 main 根目录发布，
  `.github/workflows/` 为空，非 Actions 部署）。
- 仓库：https://github.com/ethan-1900/why_jb ，线上：https://ethan-1900.github.io/why_jb/

## 发布流程

```sh
python3 scripts/subset_font.py --check   # 正文改字后必做
python3 scripts/build.py
git push origin main                     # 推送后约 1 分钟 Pages 自动构建
```

- 依赖：系统 python3（pyenv 3.9）已装 Markdown / Pillow / fontTools / brotli。
- Pages CDN 忽略 URL 查询参数，`?v=` 版本号无法刷新缓存；改动最长约 10 分钟后生效，
  想立刻验证可用不同路径（`/why_jb/index.html`）或直接换文件名。
- 沙箱下 Python 对已存在目录调用 `mkdir(exist_ok=True)` 会报 PermissionError，
  用 `mkdir(parents=True, exist_ok=True)`。

## 字体

- 正文用自托管思源宋体子集 `assets/source-han-serif-sc-subset.woff2`，只收录生成当时
  出现过的字符（当前 543 码位）。**改完文字务必跑 `scripts/subset_font.py`**，否则新字
  静默回退到系统字体，与上下文出现字形差异（曾漏「打」、后补「谓」）。
- 源字体：`~/Library/Fonts/SourceHanSerifSC-Regular.otf`。

## 配图规则

- **所有正文配图尺寸一致**：`template.html` 内联样式
  `article img{width:80%;max-width:430px;margin-left:auto;margin-right:auto}`，
  桌面端一律渲染 430px 宽，左右边缘完全对齐；窄屏统一为容器 80%。
- 用户明确要求「以倒数第二张图为标准」，标准即该 430px。不再按横竖方向区分尺寸，
  `build.py` 不给图片加任何 class，`.compact-image` 已废弃。
- 图片放 `Attachments/`，构建自动生成 `assets/optimized/*.webp` 并用 `<picture>` 回退原图。

## 背景音乐

- 页面右下角 `.bgm-toggle` 开关，音频固定路径 `assets/audio/bgm.mp3`。
- 音量 25%、1.6 秒淡入、循环；被浏览器拦截自动播放时在首次点击/按键起播；
  文件不存在则按钮自动隐藏（`error` 事件）。
- 用户希望用 Justin Bieber 的 home to mama / love yourself；版权音频未落地，
  需要用户自备文件或改用官方试听嵌入。
