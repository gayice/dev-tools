#!/usr/bin/env python3
"""
Tavily AI 搜索脚本
用法: python3 search.py "关键词" [options]
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Optional

class TavilyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('TAVILY_API_KEY', '')
        if not self.api_key:
            raise ValueError("需要提供 Tavily API Key。请设置 TAVILY_API_KEY 环境变量或在 .env 文件中配置。")
        
        self.base_url = "https://api.tavily.com"
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        include_answer: bool = True,
        include_images: bool = False,
        include_raw_content: bool = False,
        max_results: int = 5,
        include_domains: List[str] = None,
        exclude_domains: List[str] = None
    ) -> Dict:
        """
        执行 Tavily 搜索
        
        Args:
            query: 搜索查询
            search_depth: 搜索深度 (basic/advanced)
            include_answer: 是否包含AI生成的答案
            include_images: 是否包含图片
            include_raw_content: 是否包含原始网页内容
            max_results: 最大结果数量
            include_domains: 指定包含的域名列表
            exclude_domains: 指定排除的域名列表
        
        Returns:
            搜索结果字典
        """
        try:
            import requests
            
            url = f"{self.base_url}/search"
            
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": search_depth,
                "include_answer": include_answer,
                "include_images": include_images,
                "include_raw_content": include_raw_content,
                "max_results": max_results
            }
            
            if include_domains:
                payload["include_domains"] = include_domains
            if exclude_domains:
                payload["exclude_domains"] = exclude_domains
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"搜索失败: {e}", file=sys.stderr)
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Tavily AI 搜索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--depth', choices=['basic', 'advanced'], default='basic',
                        help='搜索深度（默认：basic）')
    parser.add_argument('--limit', type=int, default=5, help='最大结果数量（默认：5）')
    parser.add_argument('--no-answer', action='store_true', help='不包含AI生成的答案')
    parser.add_argument('--include-raw', action='store_true', help='包含原始网页内容')
    parser.add_argument('--include-images', action='store_true', help='包含图片')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 尝试从 .env 文件加载
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ.setdefault(key, value)
    
    try:
        # 创建客户端
        client = TavilyClient()
        
        # 执行搜索
        print(f"正在搜索: {args.query}...", file=sys.stderr)
        result = client.search(
            query=args.query,
            search_depth=args.depth,
            include_answer=not args.no_answer,
            include_images=args.include_images,
            include_raw_content=args.include_raw,
            max_results=args.limit
        )
        
        if 'error' in result:
            print(f"错误: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        # 输出结果
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n搜索关键词: {args.query}")
            print(f"找到 {len(result.get('results', []))} 条结果\n")
            print("="*80)
            
            # 显示AI生成的答案
            if 'answer' in result and result['answer']:
                print(f"\n🤖 AI 总结:\n{result['answer']}\n")
                print("="*80)
            
            # 显示搜索结果
            for i, r in enumerate(result.get('results', []), 1):
                print(f"\n{i}. {r.get('title', '无标题')}")
                print(f"   URL: {r.get('url', '')}")
                print(f"   评分: {r.get('score', 'N/A')}")
                content = r.get('content', '')
                if content:
                    print(f"   内容: {content[:150]}...")
                print()
                
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        print("\n请配置 Tavily API Key:", file=sys.stderr)
        print("1. 访问 https://tavily.com 注册账号", file=sys.stderr)
        print("2. 获取 API Key", file=sys.stderr)
        print("3. 设置环境变量: export TAVILY_API_KEY='your_key'", file=sys.stderr)
        print("4. 或在 ~/.agents/skills/tavily/.env 中配置", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
