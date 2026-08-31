import asyncio
import sys
import logging
from typing import Optional
from urllib.parse import urlparse

from agno.tools import Toolkit

logger = logging.getLogger(__name__)

# Fix for Windows asyncio subprocess issue - use ProactorEventLoop for Playwright
# ProactorEventLoop supports subprocess execution which Playwright requires
if sys.platform == 'win32':
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        logger.warning("nest_asyncio not installed. Install it with 'pip install nest-asyncio' for better Windows compatibility.")
    
    # Use ProactorEventLoop for Windows - it supports subprocess execution
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

try:
    from crawl4ai import AsyncWebCrawler, CacheMode
except ImportError as exc:  # pragma: no cover - runtime dependency
    raise ImportError(
        "`crawl4ai` is required for regulator crawling. Install it with `pip install crawl4ai`."
    ) from exc


ALLOWED_REGULATOR_DOMAINS = (
    "fda.gov",
    "ema.europa.eu",
    "pmda.go.jp",
    "cdsco.gov.in",
    "gov.uk",
    "health-canada.ca",
    "tga.gov.au",
    "pmda.jp",
    "mhra.gov.uk",
    "dcgi.gov.in",
)


class Crawl4aiTools(Toolkit):
    """
    Minimal drop-in replacement for the phi Crawl4ai toolkit.
    Restricts crawling to regulator-backed domains and returns markdown snippets.
    """

    def __init__(self, max_length: Optional[int] = 250):
        super().__init__(name="regulator_crawl4ai")
        self.max_length = max_length
        self.register(self.web_crawler)

    def web_crawler(self, url: str, max_length: Optional[int] = None) -> str:
        """Synchronously crawl an allowed URL and return truncated markdown."""
        if not url:
            return "No URL provided"

        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not any(domain.endswith(allowed) for allowed in ALLOWED_REGULATOR_DOMAINS):
            return f"Blocked non-regulator domain: {domain}"

        # Handle Windows asyncio subprocess issue safely
        try:
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(self._async_web_crawler(url, max_length or self.max_length))
            else:
                return loop.run_until_complete(self._async_web_crawler(url, max_length or self.max_length))
        except Exception as e:
            import traceback
            error_msg = f"Error crawling {url}: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return error_msg

    async def _async_web_crawler(self, url: str, max_length: Optional[int]) -> str:
        # Use thread_safe=False on Windows to avoid event loop issues
        # thread_safe=True can create tasks in different threads with different event loops
        thread_safe = False if sys.platform == 'win32' else True
        async with AsyncWebCrawler(thread_safe=thread_safe) as crawler:
            result = await crawler.arun(url=url, cache_mode=CacheMode.BYPASS)
            markdown = (result.markdown or "").strip()
            if not markdown:
                return "No result"

            snippet = markdown[:max_length] if max_length else markdown
            return snippet.replace("  ", " ")


