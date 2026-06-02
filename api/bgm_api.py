"""
番剧 API 处理模块
Bangumi 双路竞速，全败则 Jikan 兜底
"""
import asyncio
import aiohttp
from typing import List, Dict, Optional

from astrbot.api import logger
from .base_api import BaseAPI


class BGMAPI(BaseAPI):
    """番剧 API 处理类"""

    BGM_URLS = [
        "https://bgmapi.anibt.net/calendar",
        "https://api.bgm.tv/calendar",
    ]

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__(session)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    # ── Bangumi ──────────────────────────────────────

    async def _fetch_bgm(self) -> Optional[List]:
        async def _fetch(url):
            session = await self._get_session()
            async with session.get(
                url, headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if isinstance(data, list) and len(data) > 0:
                    return data
                raise ValueError("空数据")

        tasks = [asyncio.ensure_future(_fetch(u)) for u in self.BGM_URLS]
        pending = set(tasks)
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                try:
                    r = t.result()
                    logger.info("Bangumi 竞速成功")
                    for p in pending:
                        p.cancel()
                    return r
                except Exception as e:
                    logger.debug(f"Bangumi 失败: {e}")
        return None

    def _parse_bgm(self, api_data: List, max_count: int) -> List[Dict]:
        today_weekday = self._now().weekday() + 1
        anime_list = []
        for day_data in api_data:
            if not isinstance(day_data, dict):
                continue
            wid = (day_data.get("weekday") or {}).get("id")
            if wid != today_weekday:
                continue
            for item in day_data.get("items", []):
                if not isinstance(item, dict):
                    continue
                title = item.get("name_cn") or item.get("name", "")
                img = (item.get("images") or {}).get("common", "")
                if img.startswith("http://"):
                    img = "https://" + img[7:]
                if title and img:
                    anime_list.append({"title": title, "image": img})
                if len(anime_list) >= max_count:
                    break
            break
        return anime_list

    # ── 入口 ──────────────────────────────────────────

    async def get_today_anime_async(self, max_count: int = 4) -> List[Dict]:
        # 1) Bangumi 竞速
        data = await self._fetch_bgm()
        if data:
            result = self._parse_bgm(data, max_count)
            if result:
                return result

        # 2) Jikan 兜底（含中文反查）
        from .jikan_api import JikanAPI
        jikan = JikanAPI(self._session)
        jikan.set_timezone(getattr(self, '_tz', None))
        result = await jikan.get_today_anime_async(max_count)
        if result:
            return result

        # 3) 硬编码兜底
        return self._get_default_anime()

    def _get_default_anime(self) -> List[Dict]:
        _p = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E"
        return [
            {'title': '葬送的芙莉莲 第二季', 'image': _p},
            {'title': '咒术回战 涉谷事变篇', 'image': _p},
            {'title': '间谍过家家 第三季', 'image': _p},
            {'title': '鬼灭之刃 柱训练篇', 'image': _p},
        ]
