# API 概览

本页面提供了文档站点API的整体介绍和使用指南。

## API 介绍

静态文档站点提供了一系列API接口，用于获取文档内容、搜索文档和管理文档元数据。这些API设计遵循RESTful原则，使用JSON格式进行数据交换。

## API 分类

### 1. 文档内容API

提供文档的读取和查询功能，包括：

- 获取文档列表
- 获取单个文档详情
- 获取文档目录结构

### 2. 搜索API

提供全文搜索功能，支持关键词搜索、过滤和排序。

### 3. 元数据API

提供文档元数据的管理功能，包括：

- 获取文档统计信息
- 获取标签和分类信息

## 认证方式

API使用以下认证方式：

- **基本认证**：使用用户名和密码进行认证
- **API密钥认证**：使用预生成的API密钥进行认证

具体认证方式取决于您的部署配置。

## 请求格式

所有API请求都应该遵循以下格式：

```
GET/POST/PUT/DELETE /api/v1/[endpoint]
Content-Type: application/json
```

## 响应格式

所有API响应都采用JSON格式，包含以下字段：

- `success`：请求是否成功（布尔值）
- `data`：响应数据（对象或数组）
- `message`：响应消息（字符串）
- `error`：错误信息（仅在请求失败时存在）

## 错误处理

API使用HTTP状态码表示请求结果：

- `200 OK`：请求成功
- `201 Created`：资源创建成功
- `400 Bad Request`：请求参数错误
- `401 Unauthorized`：认证失败
- `403 Forbidden`：权限不足
- `404 Not Found`：资源不存在
- `500 Internal Server Error`：服务器内部错误

## 速率限制

为了保护API服务，系统实施了速率限制：

- 普通用户：每分钟60次请求
- 认证用户：每分钟300次请求

## 使用示例

### 获取文档列表

```bash
curl -X GET "http://localhost:8000/api/v1/documents" -H "Authorization: Bearer {api_key}"
```

### 搜索文档

```bash
curl -X GET "http://localhost:8000/api/v1/search?q=example" -H "Authorization: Bearer {api_key}"
```

## 下一步

- 查看 [API端点](endpoints.md) 获取详细的接口定义
- 参考 [示例](../examples/basic.md) 了解实际使用方法