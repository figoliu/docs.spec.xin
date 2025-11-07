# 安装指南

本指南将帮助您设置本地开发环境，以便运行和预览静态文档站点。

## 前提条件

在开始之前，请确保您的系统已安装以下软件：

- [Python](https://www.python.org/) 3.8 或更高版本
- [pip](https://pip.pypa.io/en/stable/installation/) 包管理器

## 步骤 1: 安装 MkDocs

使用 pip 安装 MkDocs 和 Material 主题：

```bash
pip install mkdocs mkdocs-material mkdocstrings
```

## 步骤 2: 克隆仓库

如果您尚未克隆项目仓库，请执行以下命令：

```bash
git clone [仓库URL] cd [项目目录]
```

## 步骤 3: 启动开发服务器

在项目根目录下，运行以下命令启动本地开发服务器：

```bash
mkdocs serve
```

服务器将在 http://localhost:8000 启动，您可以通过浏览器访问该地址查看文档站点。

## 步骤 4: 验证安装

如果服务器成功启动，您应该能够在浏览器中看到文档站点的首页。此时，您已经成功安装并配置了开发环境！

## 常见问题

### 端口被占用

如果 8000 端口已被占用，可以使用 `--dev-addr` 参数指定其他端口：

```bash
mkdocs serve --dev-addr=localhost:8080
```

### 依赖冲突

如果遇到依赖冲突问题，建议使用虚拟环境：

```bash
python -m venv venv source venv/bin/activate  # Linux/MacOS venv\Scripts\activate  # Windows pip install mkdocs mkdocs-material mkdocstrings
```