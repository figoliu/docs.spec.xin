# 快速入门: 构建文档静态网站

**分支**: `001-static-docs-site` | **日期**: 2025-11-07

## 概述

本指南将帮助您快速设置和使用文档静态网站系统，基于 MkDocs 和 GitHub 技术栈。

## 环境准备

### 本地开发环境

1. **安装 Python**
   - 确保安装 Python 3.11 或更高版本
   - 验证安装：`python --version` 或 `python3 --version`

2. **安装 MkDocs 和必要插件**

   ```bash
   # 创建虚拟环境（推荐）
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows

   # 安装依赖
   pip install mkdocs mkdocs-material mike
   ```

3. **克隆仓库**

   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   git checkout 001-static-docs-site
   ```

## 本地开发流程

### 启动开发服务器

```bash
# 在项目根目录
mkdocs serve
```

- 默认访问地址: http://127.0.0.1:8000
- 开发服务器支持热重载，修改文档后自动刷新

### 创建和编辑文档

1. **文档结构**
   - 所有文档存放在 `docs/` 目录下
   - 使用 Markdown 格式编写
   - 根目录的 `mkdocs.yml` 控制站点配置

2. **添加新文档**
   - 在 `docs/` 目录下创建新的 Markdown 文件
   - 在文件顶部添加 front-matter（可选但推荐）：

     ```yaml
     ---
     title: 文档标题
     language: zh-CN
     ---
     ```

3. **更新导航**
   - 编辑 `mkdocs.yml` 中的 `nav` 部分来组织文档结构

## 构建和部署

### 本地构建

```bash
# 构建静态站点
mkdocs build

# 构建输出在 site/ 目录
```

### 版本管理

使用 mike 插件管理文档版本：

```bash
# 部署新版本
mike deploy v1.0.0

# 设置默认版本
mike set-default v1.0.0

# 列出所有版本
mike list

# 部署并推送到 GitHub Pages
mike deploy v1.0.0 --push
```

## CI/CD 流程

项目使用 GitHub Actions 实现自动化构建和部署：

### 触发构建

- **主分支提交**: 自动构建并部署到主站点
- **PR 提交**: 自动构建并创建预览环境
- **标签创建**: 自动构建并创建版本化部署

### 查看构建状态

- 在 GitHub 仓库的 **Actions** 标签页查看构建历史
- PR 页面会显示预览链接（如果构建成功）

## 文档质量检查

### 运行检查工具

```bash
# 安装检查工具
pip install htmlproofer

# 运行链接检查
htmlproofer ./site

# 运行拼写检查（使用 Vale）
vale docs/
```

### 常见问题

1. **链接检查失败**
   - 检查链接格式是否正确
   - 对于相对链接，确保文件路径正确

2. **中文显示问题**
   - 确保 front-matter 中设置了 `language: zh-CN`
   - 检查 MkDocs 主题配置，确保字体支持中文

3. **构建速度慢**
   - 清理不必要的资源文件
   - 确保启用了缓存机制

## 回滚操作

### 回滚到特定版本

```bash
# 手动回滚到之前的版本
mike set-default v0.9.0 --push
```

### 通过 GitHub Actions 回滚

1. 在 GitHub 仓库中打开 Actions 标签
2. 选择 "Rollback to version" 工作流
3. 点击 "Run workflow"
4. 选择要回滚到的版本标签
5. 填写回滚原因

## 配置文件说明

### mkdocs.yml 主要配置

```yaml
site_name: Speckit中文网

# 站点配置
site_description: Speckit项目中文文档，Spec-kit中文优化，SDD相关案例分享。
site_author: Figo
site_url: https://docs.spec.xin

# 主题配置
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.suggest
  palette:
    primary: indigo
    accent: indigo

# 插件配置
plugins:
  - search
  - mkdocstrings

# 扩展配置
markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - tables

# 导航配置
nav:
  - 首页: index.md
  - 使用指南: 
    - guide/Trae.md
    - guide/VSCode.md
    - guide/CodeBuddy.md
    - guide/QCoder.md
  - SDD: 
    - SDD/SDD宣言.md
    - SDD/Openspec.md
  - 示例: 
    - examples/web应用.md
    - examples/Android应用.md
    - examples/iOS应用.md
    - examples/桌面应用.md
  - 关于: about.md
```

## 最佳实践

1. **文档组织**
   - 使用清晰的目录结构
   - 为每个主要部分创建单独的目录
   - 使用一致的命名约定

2. **内容编写**
   - 使用简洁明了的语言
   - 添加适当的示例和截图
   - 为复杂概念提供图表说明

3. **性能优化**
   - 压缩图片和资源
   - 使用适当的缓存策略
   - 避免不必要的大型依赖

## 获取帮助

- 查看 [MkDocs 官方文档](https://www.mkdocs.org/)
- 查看 [mkdocs-material 文档](https://squidfunk.github.io/mkdocs-material/)
- 查看 [mike 插件文档](https://github.com/jimporter/mike)
- 提交问题到项目的 GitHub Issues