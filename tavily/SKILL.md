---
name: tavily
description: Tavily AI 搜索工具。专为AI Agent设计的搜索API，提供结构化、高质量的搜索结果，支持实时信息检索。Use when: (1) 需要为AI提供高质量搜索结果，(2) 需要实时信息，(3) 需要结构化的搜索数据。
---

# Tavily - AI 搜索工具

Tavily 是专为 AI Agent 设计的搜索 API，提供结构化、高质量的搜索结果。

## 特点

- 🚀 专为 AI 优化的搜索结果
- 📊 结构化数据输出
- ⚡ 实时信息检索
- 🎯 高相关性结果
- 📰 支持新闻、学术、通用搜索

## 使用方法

### 命令行使用

```bash
# 基础搜索
python3 ~/.agents/skills/tavily/scripts/search.py "关键词"

# 搜索新闻
python3 ~/.agents/skills/tavily/scripts/search.py "关键词" --category news

# 搜索学术论文
python3 ~/.agents/skills/tavily/scripts/search.py "关键词" --category academic

# 限制结果数量
python3 ~/.agents/skills/tavily/scripts/search.py "关键词" --limit 5

# 包含原始内容
python3 ~/.agents/skills/tavily/scripts/search.py "关键词" --include-raw
```

### Python API

```python
from tavily import TavilyClient

# 创建客户端
client = TavilyClient(api_key="your_api_key")

# 搜索
response = client.search(
    query="OpenClaw 最新动态",
    search_depth="advanced",
    include_answer=True,
    include_images=False,
    include_raw_content=False,
    max_results=5
)

# 获取AI生成的答案
print(response['answer'])

# 获取搜索结果
for result in response['results']:
    print(f"{result['title']}: {result['url']}")
```

## 配置

设置环境变量：

```bash
export TAVILY_API_KEY="your_tavily_api_key"
```

或在 `~/.agents/skills/tavily/.env` 中配置：

```
TAVILY_API_KEY=your_tavily_api_key
```

## 获取 API Key

1. 访问 https://tavily.com
2. 注册账号
3. 在 Dashboard 中获取 API Key
4. 免费版每月 1000 次调用

## 依赖

```bash
pip install tavily-python
```

## 搜索参数

| 参数 | 类型 | 说明 |
|------|------|------|
| query | str | 搜索查询 |
| search_depth | str | 搜索深度：basic/advanced |
| include_answer | bool | 是否包含AI生成的答案 |
| include_images | bool | 是否包含图片 |
| include_raw_content | bool | 是否包含原始网页内容 |
| max_results | int | 最大结果数量 |
| include_domains | list | 指定包含的域名 |
| exclude_domains | list | 指定排除的域名 |

## 注意事项

- 需要 Tavily API Key
- 免费版有调用次数限制
- 建议缓存搜索结果以节省配额
