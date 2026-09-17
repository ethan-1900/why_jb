# Why JB

一篇关于音乐与成长的随笔，使用 GitHub Pages 托管。

## 更新文章

编辑 `Why JB.md`，图片放在 `Attachments/`，使用相对路径引用。推送到 `main` 后自动发布。原始 Markdown 和所有配图均保留；构建时会另外生成网页专用 WebP，浏览器不支持时自动回退到原图。

## 本地预览

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

打开 http://localhost:8000 。排版位于 `assets/style.css`，页面模板位于 `template.html`。

## 字体

正文用自托管的思源宋体子集 `assets/source-han-serif-sc-subset.woff2`。子集只收录生成当时文章里出现过的字，**改完文字后要重新生成**，否则新字会静默回退到系统字体，和上下文出现字形差异：

```sh
python3 scripts/subset_font.py --check   # 只报告缺字
python3 scripts/subset_font.py           # 重新生成（需本机装有 Source Han Serif SC Regular）
```

`scripts/build.py` 构建时也会检查一遍，发现缺字会打印提醒。字体内容变动后，记得同步调整 `template.html` 里 `@font-face` 的 `?v=` 版本号以刷新浏览器缓存。

## 背景音乐

页面右下角有一个背景音乐开关，音频放在 `assets/audio/bgm.mp3`（详见该目录下的说明）。进入页面会先尝试自动播放，音量 25% 并做 1.6 秒淡入；被浏览器拦截时，会在用户第一次点击 / 按键时自动起播，按钮本身也能随时播放或暂停。没有音频文件时按钮自动隐藏。
