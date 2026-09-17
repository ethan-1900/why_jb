# 背景音乐

把音频文件放成 `assets/audio/bgm.mp3`（或改 `template.html` 里 `#bgm` 的 `src`），页面右下角的播放器就会自动出现。

- 没有这个文件时，播放按钮会自动隐藏，页面其余部分不受影响。
- 建议单曲 1–3 分钟、128~192 kbps 的 mp3/m4a，控制在 5 MB 以内：GitHub 单文件上限 100 MB、仓库建议 1 GB 以内，文件越大首屏越慢。
- 音量与淡入时长在 `template.html` 的脚本里（`TARGET_VOLUME` / `FADE_MS`）。
- 注意版权：公开托管他人音乐属于向公众传播，建议使用自有录音、CC0/CC-BY 素材，或改用官方试听嵌入（YouTube / Spotify）。
