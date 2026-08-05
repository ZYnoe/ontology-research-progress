# Ontology 研究进度

用 HTML 记录研究进度，并通过 GitHub Pages 发布，方便在任何设备上访问。

## 目录结构

```
index.html                     # 首页：按日期跳转 + 全部记录列表
entries/YYYY-MM-DD.html        # 每天一篇研究记录
templates/entry-template.html  # 新记录模板
scripts/update_index.py        # 扫描 entries/ 并重新生成首页索引
assets/                        # 共享样式和脚本
```

## 添加一篇新记录

1. 复制模板：`cp templates/entry-template.html entries/2026-08-06.html`
2. 修改 `entries/2026-08-06.html`：
   - `<title>` 写成 `2026-08-06 · 记录标题`
   - `<h1>` 写标题，`.entry-date` 写日期
   - 在正文记录“今日进展 / 遇到的问题 / 下一步计划”
3. 重新生成首页索引：

   ```bash
   python3 scripts/update_index.py
   ```

4. 提交并推送：

   ```bash
   git add .
   git commit -m "add progress 2026-08-06"
   git push
   ```

## 启用 GitHub Pages

1. 将代码推送到 GitHub（仓库：`ZYnoe/ontology-research-progress`）
2. 打开仓库 Settings → Pages
3. Source 选择 **Deploy from a branch**，Branch 选择 `main`，目录选 `/ (root)`
4. 保存后稍等片刻，站点会发布到 `https://ZYnoe.github.io/ontology-research-progress/`

> 这是纯静态站点，不需要构建步骤，GitHub 会直接发布仓库里的 HTML。

## 首页用法

- 在“按日期跳转”里选择日期，点击“查看记录”即可打开当天的记录；如果那天没有记录会给出提示。
- 页面下方会按年份、月份列出全部记录，点击即可进入。
