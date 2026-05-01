#!/usr/bin/env python3
"""
多搜索引擎聚合搜索脚本
用法: python3 search.py "关键词" [options]
"""

import argparse
import json
import sys
from typing import List, Dict
import requests
from urllib.parse import quote

class MultiSearchEngine:
    def __init__(self):
        self.results = []
        
    def search_duckduckgo(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 DuckDuckGo 搜索"""
        try:
            # 尝试新的 ddgs 包名，禁用 SSL 验证以兼容 Python 3.9
            try:
                from ddgs import DDGS
                results = []
                with DDGS(verify=False) as ddgs:
                    for r in ddgs.text(query, max_results=limit):
                        results.append({
                            'title': r['title'],
                            'url': r['href'],
                            'snippet': r['body'],
                            'source': 'duckduckgo'
                        })
                return results
            except ImportError:
                from duckduckgo_search import DDGS
                results = []
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=limit):
                        results.append({
                            'title': r['title'],
                            'url': r['href'],
                            'snippet': r['body'],
                            'source': 'duckduckgo'
                        })
                return results
        except Exception as e:
            print(f"DuckDuckGo 搜索失败: {e}", file=sys.stderr)
            return []
    
    def search_brave(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 Brave Search API"""
        try:
            # 读取配置
            import os
            api_key = os.environ.get('BRAVE_API_KEY', '')
            if not api_key:
                return []
            
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": api_key
            }
            params = {
                "q": query,
                "count": limit
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            results = []
            for item in data.get('web', {}).get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('description', ''),
                    'source': 'brave'
                })
            return results
        except Exception as e:
            print(f"Brave 搜索失败: {e}", file=sys.stderr)
            return []
    
    def search(self, query: str, engines: List[str] = None, limit: int = 10) -> List[Dict]:
        """
        执行多引擎搜索
        
        Args:
            query: 搜索关键词
            engines: 指定搜索引擎列表，默认使用所有可用引擎
            limit: 每个引擎的结果数量限制
        
        Returns:
            聚合后的搜索结果列表
        """
        all_results = []
        
        # 默认使用所有引擎
        if engines is None:
            engines = ['duckduckgo', 'brave']
        
        # 执行各引擎搜索
        for engine in engines:
            if engine == 'duckduckgo':
                results = self.search_duckduckgo(query, limit)
            elif engine == 'brave':
                results = self.search_brave(query, limit)
            else:
                continue
            
            all_results.extend(results)
        
        # 去重（基于URL）
        seen_urls = set()
        unique_results = []
        for r in all_results:
            url = r['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(r)
        
        return unique_results


def main():
    parser = argparse.ArgumentParser(description='多搜索引擎聚合搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--engines', help='指定搜索引擎，逗号分隔（如：duckduckgo,brave）')
    parser.add_argument('--limit', type=int, default=10, help='每个引擎的结果数量限制（默认10）')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 解析引擎列表
    engines = None
    if args.engines:
        engines = [e.strip() for e in args.engines.split(',')]
    
    # 执行搜索
    engine = MultiSearchEngine()
    results = engine.search(args.query, engines=engines, limit=args.limit)
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n搜索关键词: {args.query}")
        print(f"找到 {len(results)} 条结果\n")
        print("="*80)
        
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['title']}")
            print(f"   来源: {r['source']}")
            print(f"   URL: {r['url']}")
            print(f"   摘要: {r['snippet'][:100]}...")
            print()


if __name__ == '__main__':
    main()
