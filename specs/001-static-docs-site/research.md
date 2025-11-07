# 研究文档: 构建文档静态网站

**分支**: `001-static-docs-site` | **日期**: 2025-11-07

## 技术决策摘要

### 静态站点生成器

**Decision**: 选择 MkDocs 作为静态站点生成器

**Rationale**: 
- MkDocs 对中文支持良好，渲染稳定
- 配置简单，学习曲线平缓
- 支持自动生成目录（Table of Contents）
- 有丰富的主题生态，特别是 mkdocs-material 主题提供了现代化的界面和搜索功能
- 与 GitHub Actions 集成简单
- 支持版本控制插件（mike）

**Alternatives considered**:
- Jekyll: GitHub Pages 默认支持，但配置相对复杂
- Hugo: 性能更好但学习曲线较陡
- Docusaurus: React 基础，功能丰富但对简单文档站可能过重

### CI/CD 平台

**Decision**: 使用 GitHub Actions

**Rationale**:
- 与 GitHub 仓库无缝集成
- 支持 PR 预览、缓存、矩阵构建等功能
- 免费额度对中小项目足够
- 配置文件（YAML）易于维护和版本控制

**Alternatives considered**:
- CircleCI: 功能强大但对免费用户有更多限制
- Jenkins: 自托管但维护成本高

### 托管平台

**Decision**: 使用 GitHub Pages 作为主要托管平台，Netlify 作为备选

**Rationale**:
- GitHub Pages 与仓库直接集成，无需额外配置
- 对公共仓库免费
- 可通过 gh-pages 分支或 docs/ 目录部署
- Netlify 作为备选提供更好的预览和回滚体验

**Alternatives considered**:
- GitLab Pages: 功能类似但项目已在 GitHub
- Vercel: 预览功能优秀但可能需要更多配置

### 文档质量检查工具

**Decision**: 
- htmlproofer 用于链接检查
- Vale 用于拼写和风格检查，配置中文规则
- 自定义脚本检查中文合规性

**Rationale**:
- htmlproofer 成熟可靠，能检测断链和无效锚点
- Vale 可扩展，支持自定义中文规则
- 组合使用能覆盖文档质量的多个方面

**Alternatives considered**:
- cSpell: 对多语言支持好但自定义规则能力有限
- language-tool: 功能全面但集成复杂度高

### 版本控制策略

**Decision**: 使用 mike 插件实现文档版本控制

**Rationale**:
- 专为 MkDocs 设计的版本控制插件
- 支持通过 Git tag 自动创建版本
- 配置简单，与 MkDocs 工作流集成
- 支持版本切换器界面

**Alternatives considered**:
- 手动维护版本目录: 灵活但维护成本高
- 其他 MkDocs 版本插件: 功能不如 mike 完善

## 技术风险评估

### 1. 中文渲染问题

**风险**: Markdown 渲染可能出现中文排版或编码问题

**缓解措施**:
- 确保 front-matter 中设置 `language: zh-CN`
- 使用支持中文的主题（如 mkdocs-material）
- 在 CI 中添加中文渲染检查

### 2. 构建性能与缓存

**风险**: 随文档增多，构建时间可能超过目标（2分钟）

**缓解措施**:
- 配置 GitHub Actions 缓存
- 实现增量构建策略
- 优化大型图片和资源

### 3. PR 预览配额限制

**风险**: 大量 PR 可能导致预览部署超出免费配额

**缓解措施**:
- 实现预览队列机制
- 设置预览自动过期策略
- 优先为活跃 PR 保留预览资源

## 依赖项版本建议

- Python: 3.11+
- MkDocs: 1.5+
- mkdocs-material: 9.5+
- mike: 1.1+
- htmlproofer: 5.0+
- Vale: 3.0+

## 最佳实践

### 文档结构

- 使用清晰的目录结构（docs/guide/, docs/reference/, docs/tutorials/）
- 为每个文档添加一致的 front-matter
- 遵循 Markdown 最佳实践（适当使用标题层级、代码块等）

### CI/CD 流程

- 使用分层缓存策略（依赖、构建产物）
- 实现构建超时和失败通知机制
- 分离构建和部署阶段以提高可靠性

### 性能优化

- 使用 CDN 加速静态资源
- 实现资源压缩和优化
- 配置适当的缓存头

### 版本管理

- 遵循语义化版本规范
- 为每个版本提供明确的变更日志
- 定期清理过时版本以控制存储成本