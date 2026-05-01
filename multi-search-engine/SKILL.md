---
name: multi-search-engine
description: 多搜索引擎聚合搜索工具。支持同时使用多个搜索引擎（Google、Bing、DuckDuckGo等）进行搜索，并聚合结果去重。Use when: (1) 需要全面的搜索结果，(2) 单一搜索引擎结果不满意，(3) 需要对比多个来源的信息。
---

# Multi Search Engine - 多搜索引擎聚合工具

支持多个搜索引擎同时搜索，聚合结果并去重。

## 支持的搜索引擎

- Google
- Bing
- DuckDuckGo
- Brave Search
- Yahoo

## 使用方法

### 命令行使用

```bash
# 使用所有搜索引擎
python3 ~/.agents/skills/multi-search-engine/scripts/search.py "关键词"

# 指定搜索引擎
python3 ~/.agents/skills/multi-search-engine/scripts/search.py "关键词" --engines google,bing

# 限制结果数量
python3 ~/.agents/skills/multi-search-engine/scripts/search.py "关键词" --limit 10

# 输出为JSON
python3 ~/.agents/skills/multi-search-engine/scripts/search.py "关键词" --format json
```

### Python API

```python
from multi_search_engine import MultiSearchEngine

# 创建搜索引擎实例
engine = MultiSearchEngine()

# 搜索
results = engine.search("OpenClaw", limit=10)

# 遍历结果
for result in results:
    print(f"{result['title']}: {result['url']}")
```

## 配置

在 `~/.agents/skills/multi-search-engine/config.json` 中配置API密钥：

```json
{
  "google_api_key": "your_google_api_key",
  "google_cx": "your_custom_search_engine_id",
  "bing_api_key": "your_bing_api_key",
  "brave_api_key": "your_brave_api_key"
}
```

## 依赖

```bash
pip install requests beautifulsoup4 duckduckgo-search googlesearch-python
```

## 注意事项

- 部分搜索引擎需要API密钥
- 建议配置多个引擎以提高搜索覆盖率
- 遵守各搜索引擎的使用条款
