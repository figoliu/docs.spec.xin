# Speckit中文网

[![GitHub license](https://img.shields.io/github/license/figoliu/docs.spec.xin)](https://github.com/figoliu/docs.spec.xin/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/figoliu/docs.spec.xin)](https://github.com/figoliu/docs.spec.xin/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/figoliu/docs.spec.xin)](https://github.com/figoliu/docs.spec.xin/network)

这是 Speckit 项目的中文文档网站，基于 MkDocs 构建，提供完整的规范文档系统和使用指南。

## 项目介绍

Speckit中文网（spec.xin）是专注于 Speckit 项目中文文档、Spec-kit 中文优化以及 SDD（软件设计文档）相关案例分享的平台。本网站基于 MkDocs 构建，支持 Markdown 语法，提供优雅的界面和强大的搜索功能。通过本系统，您可以轻松获取 Speckit 相关的技术文档、使用指南和最佳实践。

## 特性

- 基于 MkDocs 的现代化文档系统
- Material 主题，美观且响应式设计
- 内置全文搜索功能，支持高亮和建议
- 标签导航和分节导航，便于内容浏览
- 支持代码高亮、语法显示和表格
- 自动生成 API 文档（通过 mkdocstrings 插件）
- 支持多种 Markdown 扩展功能
- 自动化部署流程
- 支持 PR 预览功能

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- Git

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/figoliu/docs.spec.xin.git
cd docs.spec.xin
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 本地运行

```bash
mkdocs serve
```

访问 http://localhost:8000 查看文档网站。

## 部署方式

### 1. 独立部署

您可以将构建后的静态文件部署到任何支持静态网站托管的平台。

#### 构建静态文件

```bash
mkdocs build
```

构建后的文件将位于 `site/` 目录中。

#### 部署选项

- **Nginx**: 将 `site/` 目录配置为 Nginx 的根目录
- **Apache**: 将 `site/` 目录配置为 Apache 的根目录
- **Netlify**: 连接 GitHub 仓库，设置构建命令为 `mkdocs build`，发布目录为 `site`
- **Vercel**: 连接 GitHub 仓库，设置构建命令为 `mkdocs build`，发布目录为 `site`

### 2. GitHub Pages 托管

本项目已配置 GitHub Actions 工作流，支持自动部署到 GitHub Pages。

#### 自动部署

当您推送到 `main` 分支时，GitHub Actions 将自动：
1. 构建文档
2. 部署到 GitHub Pages

#### 手动触发部署

您也可以通过 GitHub Actions 页面手动触发工作流：

1. 访问项目的 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Deploy Documentation" 工作流
4. 点击 "Run workflow" 按钮

#### 配置说明

GitHub Pages 的部署由以下两个工作流文件控制：

- `.github/workflows/deploy.yml`: 处理文档部署到 GitHub Pages
- `.github/workflows/docs-site.yml`: 处理构建、质量检查和 PR 预览

## 目录结构

```
├── docs/              # Markdown 文档源文件
│   ├── guide/         # 使用指南（Trae、VSCode、CodeBuddy、QCoder）
│   ├── SDD/           # SDD 相关文档
│   ├── examples/      # 示例代码（Web、Android、iOS、桌面应用）
│   └── index.md       # 首页
├── site/              # 构建后的静态文件
├── specs/             # 规范文档
│   └── 001-static-docs-site/  # 静态文档站点规范
├── mkdocs.yml         # MkDocs 配置文件
└── requirements.txt   # Python 依赖
```

## 文档编写

### 添加新文档

1. 在 `docs/` 目录下创建新的 Markdown 文件
2. 在 `mkdocs.yml` 中更新导航配置
3. 提交更改并推送到仓库

### Markdown 语法

本项目支持标准 Markdown 语法以及一些扩展功能，包括：

- 代码块与语法高亮
- 表格
- 任务列表
- 脚注
- 目录

## 贡献指南

我们欢迎任何形式的贡献！如果您想为项目做出贡献，请：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有任何问题或建议，请在 GitHub 仓库中提交 Issue。