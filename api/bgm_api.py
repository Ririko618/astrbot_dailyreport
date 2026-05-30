"""
BGM (Bangumi) API 处理模块
用于获取今日新番数据，供日报模板使用
"""
import aiohttp
from datetime import datetime
from typing import List, Dict, Optional

from astrbot.api import logger
from .base_api import BaseAPI


class BGMAPI(BaseAPI):
    """BGM API 处理类"""
    
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """
        初始化
        
        Args:
            session: 可选的 aiohttp.ClientSession，如果提供则复用
        """
        super().__init__(session)
        self.url = "https://api.bgm.tv/calendar"
        self.fallback_url = "https://bgmapi.anibt.net/calendar"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def get_calendar_async(self) -> Optional[List]:
        """
        异步方式获取 BGM 日历数据。主地址失败时自动尝试备用地址。

        Returns:
            API 返回的原始数据，失败返回 None
        """
        for url in (self.url, self.fallback_url):
            try:
                session = await self._get_session()
                async with session.get(
                    url,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    response.raise_for_status()
                    logger.info(f"BGM API 请求成功: {url}")
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.warning(f"请求 BGM API 失败 ({url}): {e}")
            except Exception as e:
                logger.error(f"获取 BGM 数据失败 ({url}): {e}", exc_info=True)
        return None
    
    def parse_today_anime(self, api_data: Optional[List], max_count: int = 4) -> List[Dict]:
        """
        解析 BGM 数据，提取今日新番

        Args:
            api_data: API 返回的原始数据
            max_count: 最多返回几个新番

        Returns:
            格式化的新番列表，格式：
            [
                {
                    'title': '动画名称',
                    'image': '图片URL'
                },
                ...
            ]
        """
        if not api_data or not isinstance(api_data, list):
            logger.warning(f"BGM API 数据无效: type={type(api_data).__name__}, len={len(api_data) if api_data else 0}")
            return self._get_default_anime()

        try:
            today_weekday = datetime.now().weekday() + 1
            logger.info(f"今日星期ID: {today_weekday}, API 返回 {len(api_data)} 天的数据")

            anime_list = []

            for day_data in api_data:
                if not isinstance(day_data, dict):
                    continue

                weekday_info = day_data.get('weekday', {})
                weekday_id = weekday_info.get('id')
                items = day_data.get('items', [])

                if weekday_id == today_weekday:
                    logger.info(f"匹配到今天(weekday_id={weekday_id}), {len(items)} 个条目")

                    for item in items:
                        if not isinstance(item, dict):
                            continue

                        name_cn = item.get('name_cn', '')
                        name_jp = item.get('name', '')
                        title = name_cn if name_cn else name_jp

                        images = item.get('images', {})
                        image_url = images.get('common', '')
                        if image_url and image_url.startswith('http://'):
                            image_url = 'https://' + image_url[7:]

                        if title and image_url:
                            anime_list.append({
                                'title': title,
                                'image': image_url
                            })

                        if len(anime_list) >= max_count:
                            break

                    break

            if len(anime_list) == 0:
                logger.warning("未找到今日新番数据，使用默认数据")
                return self._get_default_anime()

            return anime_list

        except Exception as e:
            logger.error(f"解析 BGM 数据时出错: {e}", exc_info=True)
            return self._get_default_anime()
    
    def _get_default_anime(self) -> List[Dict]:
        """
        返回默认的新番数据（当 API 失败时使用）
        使用透明 SVG 占位图，CSS 背景色会自然透出
        """
        _placeholder = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E"
        return [
            {'title': '葬送的芙莉莲 第二季', 'image': _placeholder},
            {'title': '咒术回战 涉谷事变篇', 'image': _placeholder},
            {'title': '间谍过家家 第三季', 'image': _placeholder},
            {'title': '鬼灭之刃 柱训练篇', 'image': _placeholder},
        ]
    
    async def get_today_anime_async(self, max_count: int = 4) -> List[Dict]:
        """
        异步方式获取今日新番数据（推荐用于 AstrBot）
        
        Args:
            max_count: 最多返回几个新番
            
        Returns:
            格式化的今日新番列表
        """
        api_data = await self.get_calendar_async()
        return self.parse_today_anime(api_data, max_count)
