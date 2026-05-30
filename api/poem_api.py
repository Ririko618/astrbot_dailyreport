"""
每日古诗词 API 处理模块
"""
import aiohttp
from typing import Optional, Dict

from astrbot.api import logger
from .base_api import BaseAPI


class PoemAPI(BaseAPI):
    """每日古诗词 API 处理类"""

    def __init__(self, token: str, session: Optional[aiohttp.ClientSession] = None):
        super().__init__(session)
        self.url = "https://v3.alapi.cn/api/shici"
        self.token = token
        self.headers = {"Content-Type": "application/json"}

    def _get_default_poem(self) -> Dict[str, str]:
        return {
            'content': '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
            'from': '李白'
        }

    async def get_poem_async(self) -> Dict[str, str]:
        """异步获取每日古诗词"""
        try:
            session = await self._get_session()
            params = {"token": self.token}
            async with session.get(
                self.url,
                headers=self.headers,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                code = data.get("code")
                success = data.get("success", False)

                if (code == 200 or success) and data.get("data"):
                    poem = data["data"]
                    content = poem.get("content", "").strip()
                    author = poem.get("author", "").strip() or "未知"
                    source = poem.get("source", "").strip()

                    if source:
                        content += f"\n——《{source}》"

                    return {
                        'content': content or self._get_default_poem()['content'],
                        'from': author
                    }
                else:
                    logger.warning(f"古诗词API返回异常: code={code}, message={data.get('message', '')}")
                    return self._get_default_poem()
        except Exception as e:
            logger.error(f"获取每日古诗词失败: {e}", exc_info=True)
            return self._get_default_poem()
