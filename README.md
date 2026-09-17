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
