# Implementation Notes — 构建文档静态网站（实现示例）

此文件包含平台、CI 与工具示例，供实现团队参考。主规范 (`spec.md`) 保持技术中立，具体实现细节写在此处。

## 托管平台示例

- GitHub Pages: 适合直接从 repo 发布静态站点，支持通过 `gh-pages` 分支或 `docs/` 目录托管。优点：与 GitHub 集成无缝、免费（公共仓库）。限制：对私有内容及回滚策略需额外配置。
- Netlify: 支持分支预览、快速回滚和自定义域名，内置 CDN。优点：预览 URL 易于集成到 PR。限制：有免费额度/带宽限制。

注意：以上仅为示例。选择哪种平台应基于成本、访问控制与团队熟悉度。平台具体配置步骤、环境变量与凭据存放方式应写入 plan.md 或 CI 配置仓库密钥文档。

## CI 与预览部署（示例）

- 推荐使用 GitHub Actions 或类似 CI 来实现构建与预览流程：
  - 主分支/标签触发常规站点构建并发布到主站托管路径。
  - PR 构建触发预览部署并产出 `preview_url`（部署到 Netlify/临时托管或使用 Actions artifact + preview 服务）。

- 建议的 CI 步骤（参考顺序）：
  1. checkout
  2. restore cache
  3. install deps
  4. build site
  5. run doc-quality checks (link-checker, spell-checker, chinese-check)
  6. deploy preview or publish
  7. post status/PR comment with `preview_url` / build logs

## 文档质量检查工具（示例）

- link-checker: htmlproofer、broken-link-checker 或专用工具。
- 拼写检查: Vale（可扩展规则）、cSpell（针对多语言）、或结合 language-tool 服务。
- 中文合规性/质量: 自定义脚本（检测 language front-matter、中文字符占比、术语一致性）或 Vale 的中文规则集。

## 建议的验收测试自动化位置

- 将验收测试集成到 `specs/001-static-docs-site/tests/`，并在 CI 中提供一个 `smoke` 阶段用于运行关键 FR 的自动化验收步骤（例如 FR-001、FR-003 的端到端触发与可访问性检查）。

## 费用与配额注意事项

- 评估 CI/预览对免费额度的消耗（例如 Actions 分钟、Netlify 部署次数），并定义队列策略以限制并发预览。

## 迁移/回滚建议

- 对每次发布保留部署记录与构建 artifact；提供快速回滚脚本或利用平台的回滚功能。针对历史版本保留策略（例如保留最近 N 个版本）应在发布策略中定义并在成本估算中体现。
