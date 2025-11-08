# 高级指南

本指南介绍静态文档站点的高级功能和使用技巧。

## 文档组织最佳实践

### 目录结构

为了保持文档的清晰性和可维护性，建议按照以下结构组织文档：

```
docs/
  ├── guide/         # 使用指南
  ├── api/           # API参考
  ├── examples/      # 示例代码
  └── index.md       # 首页
```

### 命名约定

- 使用小写字母和连字符（-）命名文件和目录
- 文件名应该简洁明了，反映文件内容
- 避免使用特殊字符和空格

## 高级 Markdown 功能

### 提示框（Admonitions）

Material 主题支持多种类型的提示框：

```markdown
!!! note "注意"
    这是一条普通提示信息

!!! warning "警告"
    这是一条警告信息

!!! danger "危险"
    这是一条危险信息

!!! success "成功"
    这是一条成功信息

!!! info "信息"
    这是一条信息提示
```

### 标签页（Tabs）

使用标签页可以在有限空间内展示不同的内容：

```markdown
=== "Python"
    ```python
    print("Hello, world!")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello, world!");
    ```

=== "Java"
    ```java
    System.out.println("Hello, world!");
    ```
```

## 搜索索引优化

为了提高搜索质量，可以：

1. 在文档开头添加清晰的标题和简介
2. 使用描述性的段落标题
3. 在适当位置使用关键词，但避免关键词堆砌
4. 为代码块添加语言标识，便于搜索

## 自定义主题

如果需要自定义站点主题，可以在 `mkdocs.yml` 中进行配置：

```yaml
theme:
  name: material
  custom_dir: docs/overrides
  palette:
    primary: indigo
    accent: indigo
    scheme: slate
  font:
    text: Roboto
    code: Roboto Mono
```

然后在 `docs/overrides` 目录中创建自定义模板和样式。

## 构建和部署

### 构建静态站点

运行以下命令生成静态站点文件：

```bash
mkdocs build
```

生成的文件将位于 `site` 目录中。

### 部署到 GitHub Pages

可以使用 GitHub Actions 自动部署：

1. 在 `.github/workflows/` 目录下创建部署配置文件
2. 配置工作流以在提交后自动构建和部署

详细配置请参考 [部署指南](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)。

## 性能优化

### 减少页面加载时间

- 优化图片大小和格式
- 避免在单页中包含过多内容
- 使用适当的缓存策略
- 考虑使用CDN分发静态资源

### 提高搜索性能

- 限制单个文档的大小
- 使用清晰的文档结构和层次
- 避免重复内容

## 故障排除

### 常见问题

#### 站点构建失败

- 检查 Markdown 语法是否正确
- 确保导航配置中的文件路径正确
- 检查插件安装是否完整

#### 搜索不工作

- 确保 `search` 插件在配置中启用
- 检查文档内容是否包含足够的可搜索文本
- 尝试重新构建站点