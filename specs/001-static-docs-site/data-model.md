# 数据模型: 构建文档静态网站

**分支**: `001-static-docs-site` | **日期**: 2025-11-07

## 实体定义

### Document (文档)

**描述**: 表示仓库中的单个 Markdown 文档

**关键属性**:
- `path`: 字符串，文档在仓库中的相对路径（例如 `docs/guide/getting-started.md`）
- `title`: 字符串，文档标题（从 front-matter 或一级标题提取）
- `language`: 字符串，文档语言（默认为 `zh-CN`）
- `last_modified`: 日期时间，最后修改时间（从 Git 提交记录获取）
- `author`: 字符串，最后修改者（从 Git 提交记录获取）
- `content`: 字符串，Markdown 内容
- `front_matter`: 对象，文档的元数据（YAML 解析后）
- `toc`: 数组，目录结构（自动生成）

**验证规则**:
- `path` 必须唯一且符合仓库路径规范
- `language` 必须为有效的语言代码（如 `zh-CN`, `en-US`）
- 文档内容不能为空

### SiteBuild (站点构建)

**描述**: 一次构建事件

**关键属性**:
- `id`: 字符串，构建唯一标识符
- `branch`: 字符串，触发构建的分支名称
- `commit`: 字符串，触发构建的提交哈希
- `status`: 字符串，构建状态（`queued`, `running`, `success`, `failed`）
- `started_at`: 日期时间，构建开始时间
- `finished_at`: 日期时间，构建结束时间
- `logs_url`: 字符串，构建日志 URL
- `deployed_url`: 字符串，部署后的站点 URL（成功时）
- `error_details`: 字符串，错误详情（失败时）

**验证规则**:
- 每个构建必须关联到一个有效的分支和提交
- 构建状态转换必须符合逻辑（queued → running → success/failed）

### Preview (预览)

**描述**: PR 关联的预览部署

**关键属性**:
- `preview_url`: 字符串，预览站点的访问 URL
- `pr_number`: 整数，关联的 PR 编号
- `build_id`: 字符串，关联的 SiteBuild ID
- `expires_at`: 日期时间，预览过期时间
- `created_at`: 日期时间，预览创建时间
- `status`: 字符串，预览状态（`active`, `expired`, `deleted`）

**验证规则**:
- 每个预览必须关联到一个有效的 PR 和构建
- 预览 URL 必须可访问

### Version (版本)

**描述**: 标记发布的文档版本

**关键属性**:
- `tag`: 字符串，版本标签（符合语义化版本规范，如 `v1.0.0`）
- `release_date`: 日期时间，发布日期
- `build_id`: 字符串，关联的 SiteBuild ID
- `description`: 字符串，版本描述
- `is_latest`: 布尔值，是否为最新版本
- `is_default`: 布尔值，是否为默认版本

**验证规则**:
- 版本标签必须唯一且符合语义化版本规范
- 每个版本必须关联到一个成功的构建

## 关系

- 一个 `Document` 可以属于多个 `Version`
- 一个 `SiteBuild` 可以生成一个或多个 `Preview`
- 一个 `Version` 关联到一个 `SiteBuild`
- 一个 `Preview` 关联到一个 `SiteBuild` 和一个 PR

## 状态转换

### SiteBuild 状态转换

```
queued → running → success
      → running → failed
```

### Preview 状态转换

```
active → expired → deleted
```

## 数据存储

- **文档**: 存储在 Git 仓库中作为 Markdown 文件
- **构建信息**: 存储在 GitHub Actions 工作流日志和状态中
- **预览信息**: 存储在 GitHub Actions 输出和 PR 注释中
- **版本信息**: 存储在 Git tag 和 GitHub Release 中
- **派生数据**: 
  - HTML 输出: 存储在 `gh-pages` 分支或部署平台
  - 搜索索引: 作为静态文件包含在构建输出中

## 数据流程图

```
+-------------+    触发    +-------------+    生成    +-------------+
|  Git 提交   | ---------> |  SiteBuild  | ---------> | HTML/静态资源 |
+-------------+            +-------------+            +-------------+
        |                         |                        |
        | 触发(PR)                | 关联                   | 部署
        v                         v                        v
+-------------+    生成    +-------------+    部署    +-------------+
| GitHub PR   | ---------> |   Preview   | ---------> |  预览站点    |
+-------------+            +-------------+            +-------------+

+-------------+    标记    +-------------+    部署    +-------------+
| Git Release | ---------> |   Version   | ---------> |  正式站点    |
+-------------+            +-------------+            +-------------+
```