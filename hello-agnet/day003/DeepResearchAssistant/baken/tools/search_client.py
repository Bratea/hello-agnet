#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
搜索调度服务
"""
import hashlib
import json
import logging
from pathlib import Path
from typing import List, Optional

from hello_agents.tools import SearchTool

from config import Configuration

logger = logging.getLogger(__name__)


class SearchClient:
    """
搜索调度客户端
"""

    def __init__(self, config: Configuration):
        self.config = config
        self.search_tool = SearchTool(backend="hybrid")

        # 缓存目录
        self.cache_dir = Path("./cache/search")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search(
        self,
        query: str,
        max_results: int = 5,
        use_cache: bool = True
    ) -> List[dict]:
        """执行搜索（带缓存）

        Args:
            query: 搜索查询
            max_results: 最大结果数量
            use_cache: 是否使用缓存

        Returns:
            搜索结果列表
        """
        # 尝试从缓存读取
        if use_cache:
            cached = self._read_cache(query, max_results)
            if cached is not None:
                return cached

        # 执行搜索
        results = self._execute_search(query, max_results)

        # 保存到缓存
        if use_cache and results:
            self._write_cache(query, max_results, results)

        return results

    def _execute_search(self, query: str, max_results: int) -> List[dict]:
        """实际执行搜索"""
        try:
            raw_response = self.search_tool.run({
                "input": query,
                "backend": self.config.search_api.value,
                "mode": "structured",
                "max_results": max_results
            })

            results = raw_response.get("results", []) if isinstance(raw_response, dict) else []

            results = self._deduplicate_sources(results)
            results = self._limit_source_tokens(results)

            logger.info(f"搜索成功：{query}，返回{len(results)}个结果")
            return results

        except Exception as e:
            logger.error(f"搜索失败：{query}，错误：{e}")
            return []

    def _deduplicate_sources(self, sources: List[dict]) -> List[dict]:
        """去除重复的URL"""
        seen_urls = set()
        unique_sources = []
        for source in sources:
            url = source.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append(source)
        return unique_sources

    def _limit_source_tokens(
        self,
        sources: List[dict],
        max_tokens_per_source: int = 2000
    ) -> List[dict]:
        """限制每个来源的Token数量"""
        limited_sources = []
        for source in sources:
            snippet = source.get("snippet", "")
            max_chars = max_tokens_per_source * 4
            if len(snippet) > max_chars:
                snippet = snippet[:max_chars] + "..."
            limited_sources.append({**source, "snippet": snippet})
        return limited_sources

    # ---- 缓存相关 ----

    def _cache_path(self, query: str, max_results: int) -> Path:
        """生成缓存文件路径"""
        raw = f"{query}_{max_results}_{self.config.search_api.value}"
        key = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return self.cache_dir / f"{key}.json"

    def _read_cache(self, query: str, max_results: int) -> Optional[List[dict]]:
        """读取缓存"""
        path = self._cache_path(query, max_results)
        if not path.exists():
            return None
        try:
            logger.info(f"从缓存读取搜索结果：{query}")
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"缓存读取失败：{e}")
            return None

    def _write_cache(self, query: str, max_results: int, results: List[dict]) -> None:
        """写入缓存"""
        path = self._cache_path(query, max_results)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        except OSError as e:
            logger.warning(f"缓存写入失败：{e}")