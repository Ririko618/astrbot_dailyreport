"""
Jikan API 兜底模块
当 Bangumi 不可用时，从 Jikan 获取番剧并通过 AniList 反查中文名
"""
import asyncio
import aiohttp
from typing import List, Dict, Optional

from astrbot.api import logger
from .base_api import BaseAPI


class JikanAPI(BaseAPI):
    """Jikan 兜底，通过 AniList 反查中文名"""

    JIKAN_URL = "https://api.jikan.moe/v4/schedules"
    ANILIST_URL = "https://graphql.anilist.co"
    WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__(session)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def get_today_anime_async(self, max_count: int = 4) -> Optional[List[Dict]]:
        """获取今日番剧并通过 AniList 反查中文名，全败返回 None"""
        today = self.WEEKDAYS[self._now().weekday()]
        url = f"{self.JIKAN_URL}?filter={today}"

        session = await self._get_session()
        try:
            async with session.get(
                url, headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except Exception as e:
            logger.warning(f"Jikan 请求失败: {e}")
            return None

        items = (data or {}).get("data", [])
        if not items:
            return None

        logger.info(f"Jikan 获取 {len(items)} 部番剧，通过 AniList 反查中文名...")

        # 并发反查
        async def _resolve(item):
            title = item.get("title", "")
            jpg = (item.get("images") or {}).get("jpg", {})
            img = jpg.get("large_image_url") or jpg.get("image_url", "")
            if not title or not img:
                return None
            cn = await self._anilist_search(title)
            return {"title": cn or title, "image": img}

        tasks = [_resolve(item) for item in items[:max_count * 2]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        final = [r for r in results if isinstance(r, dict) and r.get("title") and r.get("image")][:max_count]
        return final if final else None

    async def _anilist_search(self, keyword: str) -> Optional[str]:
        """通过 AniList GraphQL 搜索中文标题"""
        query = """
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            title {
              romaji
              native
            }
          }
        }
        """
        try:
            session = await self._get_session()
            async with session.post(
                self.ANILIST_URL,
                json={"query": query, "variables": {"search": keyword}},
                headers={**self.headers, "Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=8)
            ) as resp:
                if resp.status != 200:
                    return None
                result = await resp.json()
                media = (result.get("data") or {}).get("Media")
                if not media:
                    return None
                title = media.get("title") or {}
                # native 往往是日文汉字，中文用户大多能看懂
                return title.get("native") or title.get("romaji")
        except Exception:
            return None
