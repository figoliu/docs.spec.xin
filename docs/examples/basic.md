# 基本示例

本页面提供了静态文档站点的基本使用示例。

## 文档编写示例

### Markdown 基础

以下是一些基本的 Markdown 语法示例：

#### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
```

#### 文本格式

```markdown
**粗体文本**
*斜体文本*
***粗斜体文本***
~~删除线~~
```

#### 列表

**无序列表：**
```markdown
- 项目一
- 项目二
  - 子项目一
  - 子项目二
- 项目三
```

**有序列表：**
```markdown
1. 第一步
2. 第二步
3. 第三步
```

#### 链接

```markdown
[MkDocs官网](https://www.mkdocs.org/)
```

#### 图片

```markdown
![示例图片](https://via.placeholder.com/150)
```

#### 表格

```markdown
| 名称 | 描述 | 价格 |
|------|------|------|
| 产品A | 基础版本 | $10 |
| 产品B | 高级版本 | $20 |
| 产品C | 专业版本 | $30 |
```

### Material 主题特有功能

#### 提示框

```markdown
!!! note
    这是一个普通提示框

!!! warning
    这是一个警告提示框

!!! success
    这是一个成功提示框

!!! danger
    这是一个危险提示框

!!! info
    这是一个信息提示框
```

#### 可折叠内容

```markdown
??? "点击展开更多信息"
    这里是展开后显示的内容。
    可以包含多行文本、代码块等。
```

#### 代码高亮

```python
# Python 代码示例
def hello_world():
    print("Hello, World!")

hello_world()
```

```javascript
// JavaScript 代码示例
function helloWorld() {
    console.log("Hello, World!");
}

helloWorld();
```

## 站点配置示例

### mkdocs.yml 基本配置

以下是 `mkdocs.yml` 文件的基本配置示例：

```yaml
site_name: 我的文档站点
site_description: 这是一个文档站点示例
theme:
  name: material
  features:
    - navigation.tabs
    - search.highlight
    - search.suggest
plugins:
  - search
markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
nav:
  - 首页: index.md
  - 指南: guide.md
  - API: api.md
```

## 本地开发示例

### 启动开发服务器

```bash
# 安装依赖
pip install mkdocs mkdocs-material

# 克隆仓库
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# 启动开发服务器
mkdocs serve
```

### 构建站点

```bash
# 构建静态站点文件
mkdocs build

# 预览构建结果
python -m http.server --directory site
```

## 搜索功能使用示例

### 基本搜索

1. 在文档站点右上角找到搜索框
2. 输入关键词，如 "安装"
3. 按 Enter 键或点击搜索图标
4. 浏览搜索结果，点击感兴趣的条目

### 高级搜索技巧

- **精确匹配**：使用引号包围关键词，如 `"安装指南"`
- **排除关键词**：使用减号前缀，如 `安装 -高级`
- **多关键词搜索**：使用空格分隔多个关键词，如 `配置 示例`
- **通配符搜索**：使用星号作为通配符，如 `配置*`

## 下一步

- 查看 [高级示例](advanced.md) 了解更多高级功能
- 参考 [API参考](../api/overview.md) 获取接口详情
- 阅读 [高级指南](../guide/advanced.md) 学习进阶技巧