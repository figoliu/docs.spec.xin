# API 端点

本页面详细列出了文档站点API的所有端点及其使用方法。

## 1. 文档内容API

### 1.1 获取文档列表

**端点**：`GET /api/v1/documents`

**参数**：
- `category`（可选）：文档分类
- `tag`（可选）：文档标签
- `limit`（可选）：返回结果数量限制，默认100
- `offset`（可选）：结果偏移量，默认0

**响应示例**：
```json
{
  "success": true,
  "data": [
    {
      "id": "doc123",
      "title": "安装指南",
      "path": "guide/installation.md",
      "category": "guide",
      "tags": ["installation", "setup"],
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "doc456",
      "title": "快速入门",
      "path": "guide/quickstart.md",
      "category": "guide",
      "tags": ["quickstart", "tutorial"],
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ],
  "message": "获取文档列表成功",
  "total": 10
}
```

### 1.2 获取文档详情

**端点**：`GET /api/v1/documents/{id}`

**参数**：
- `id`（必需）：文档ID或路径

**响应示例**：
```json
{
  "success": true,
  "data": {
    "id": "doc123",
    "title": "安装指南",
    "path": "guide/installation.md",
    "content": "# 安装指南\n\n本指南将帮助您设置本地开发环境...",
    "html_content": "<h1>安装指南</h1><p>本指南将帮助您设置本地开发环境...</p>",
    "category": "guide",
    "tags": ["installation", "setup"],
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  "message": "获取文档详情成功"
}
```

### 1.3 获取目录结构

**端点**：`GET /api/v1/documents/structure`

**响应示例**：
```json
{
  "success": true,
  "data": {
    "title": "文档站点",
    "items": [
      {
        "title": "首页",
        "path": "index.md",
        "type": "file"
      },
      {
        "title": "使用指南",
        "type": "section",
        "items": [
          {
            "title": "安装指南",
            "path": "guide/installation.md",
            "type": "file"
          },
          {
            "title": "快速入门",
            "path": "guide/quickstart.md",
            "type": "file"
          }
        ]
      }
    ]
  },
  "message": "获取目录结构成功"
}
```

## 2. 搜索API

### 2.1 搜索文档

**端点**：`GET /api/v1/search`

**参数**：
- `q`（必需）：搜索关键词
- `category`（可选）：文档分类过滤
- `tag`（可选）：文档标签过滤
- `highlight`（可选）：是否高亮匹配文本，默认true
- `limit`（可选）：返回结果数量限制，默认20

**响应示例**：
```json
{
  "success": true,
  "data": {
    "query": "installation",
    "results": [
      {
        "id": "doc123",
        "title": "安装指南",
        "path": "guide/installation.md",
        "snippet": "本指南将帮助您设置<span class=\"highlight\">安装</span>本地开发环境...",
        "score": 0.95
      },
      {
        "id": "doc789",
        "title": "高级指南",
        "path": "guide/advanced.md",
        "snippet": "在进行高级配置前，请确保已完成基础<span class=\"highlight\">安装</span>...",
        "score": 0.72
      }
    ],
    "total": 5
  },
  "message": "搜索成功"
}
```

## 3. 元数据API

### 3.1 获取文档统计

**端点**：`GET /api/v1/stats`

**响应示例**：
```json
{
  "success": true,
  "data": {
    "total_documents": 50,
    "total_categories": 5,
    "total_tags": 20,
    "last_updated": "2023-01-01T00:00:00Z",
    "document_count_by_category": {
      "guide": 20,
      "api": 15,
      "examples": 10,
      "about": 5
    }
  },
  "message": "获取统计信息成功"
}
```

### 3.2 获取所有标签

**端点**：`GET /api/v1/tags`

**响应示例**：
```json
{
  "success": true,
  "data": [
    {
      "name": "installation",
      "count": 5
    },
    {
      "name": "tutorial",
      "count": 8
    },
    {
      "name": "api",
      "count": 12
    }
  ],
  "message": "获取标签列表成功"
}
```

## 4. 访问控制API

### 4.1 用户认证

**端点**：`POST /api/v1/auth/login`

**参数**：
- `username`（必需）：用户名
- `password`（必需）：密码

**响应示例**：
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": "2023-01-01T00:00:00Z",
    "user": {
      "id": "user123",
      "username": "admin",
      "roles": ["admin", "editor"]
    }
  },
  "message": "登录成功"
}
```

### 4.2 验证API密钥

**端点**：`GET /api/v1/auth/verify`

**参数**：
- `Authorization` 头：`Bearer {api_key}`

**响应示例**：
```json
{
  "success": true,
  "data": {
    "valid": true,
    "expires_at": "2023-01-01T00:00:00Z",
    "permissions": ["read:documents", "search:documents"]
  },
  "message": "API密钥验证成功"
}
```

## 错误响应示例

**400 Bad Request**
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "请求参数错误",
    "details": "缺少必需参数: q"
  }
}
```

**401 Unauthorized**
```json
{
  "success": false,
  "error": {
    "code": 401,
    "message": "认证失败",
    "details": "无效的API密钥"
  }
}
```

**404 Not Found**
```json
{
  "success": false,
  "error": {
    "code": 404,
    "message": "资源不存在",
    "details": "文档ID不存在"
  }
}