# 高级示例

本页面提供了静态文档站点的高级使用示例和技巧。

## 自定义主题配置

### 高级主题设置

以下是 `mkdocs.yml` 中的高级主题配置示例：

```yaml
theme:
  name: material
  custom_dir: docs/overrides  # 自定义模板目录
  logo: assets/images/logo.png
  favicon: assets/images/favicon.ico
  icon:
    logo: material/library
    repo: fontawesome/brands/github
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.tracking
    - search.highlight
    - search.suggest
    - search.share
    - content.code.annotate
    - content.code.copy
    - content.tabs.link
    - content.footnote.tooltips
    - content.action.edit
    - header.autohide
  palette:
    # 浅色模式
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: 切换到深色模式
    # 深色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/weather-sunny
        name: 切换到浅色模式
  font:
    text: Roboto
    code: Roboto Mono
  language: zh
```

### 自定义CSS

在 `docs/overrides/assets/stylesheets/` 目录中创建 `custom.css` 文件：

```css
/* 自定义全局样式 */
:root {
  --md-primary-fg-color: #4f46e5;
  --md-accent-fg-color: #4f46e5;
}

/* 自定义标题样式 */
h1, h2, h3 {
  font-weight: 600;
}

/* 自定义代码块样式 */
.md-code {
  font-size: 0.9rem;
}

/* 自定义提示框样式 */
.admonition {
  border-radius: 6px;
}

/* 自定义表格样式 */
.md-typeset__table {
  font-size: 0.9rem;
}

.md-typeset table:not([class]) th {
  background-color: rgba(79, 70, 229, 0.1);
}
```

## 插件配置示例

### 常用插件配置

```yaml
plugins:
  # 搜索插件
  - search:
      lang: zh
      separator: '\\s+|,|\\.|;|\\:|!|\
|\\(|\\)|\