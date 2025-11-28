"""AI extraction service using Google Gemini."""
import logging
import json
import re
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import google.generativeai as genai

from app.config import settings
from app.schemas.tender import TenderExtractModel

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


class ExtractionService:
    """Service for extracting structured data from tender announcements using AI."""

    def __init__(self) -> None:
        """Initialize extraction service."""
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": settings.gemini_temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
            system_instruction=self._get_system_instruction(),
        )

    def _get_system_instruction(self) -> str:
        """Get system instruction for the AI model."""
        return """你是一个专业的招标信息提取助手。你的任务是从招标公告文本中提取关键信息，并以JSON格式返回。

提取规则:
1. 项目名称 (project_name): 招标项目的完整名称
2. 预算金额 (budget_amount): 数字，单位为人民币元。如果是"万元"需要乘以10000
3. 预算货币 (budget_currency): 默认"CNY"
4. 截止时间 (deadline): ISO 8601格式的日期时间，例如"2024-12-31T17:00:00"
5. 联系人 (contact_person): 联系人姓名
6. 联系电话 (contact_phone): 电话号码
7. 联系邮箱 (contact_email): 电子邮箱地址
8. 地点 (location): 项目所在地或送达地点

输出格式:
严格返回JSON对象，不要包含任何额外说明。如果某个字段无法提取，使用null。

示例输入:
"某市政府办公设备采购项目招标公告
项目名称: 办公电脑及打印机采购
预算金额: 50万元
投标截止时间: 2024年12月25日17:00
联系人: 张三
电话: 010-12345678
邮箱: zhangsan@example.com
送达地点: 北京市朝阳区"

示例输出:
{
  "project_name": "办公电脑及打印机采购",
  "budget_amount": 500000,
  "budget_currency": "CNY",
  "deadline": "2024-12-25T17:00:00",
  "contact_person": "张三",
  "contact_phone": "010-12345678",
  "contact_email": "zhangsan@example.com",
  "location": "北京市朝阳区"
}"""

    @retry(
        stop=stop_after_attempt(settings.scraper_max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def extract(self, title: str, content: str) -> Optional[TenderExtractModel]:
        """
        Extract structured information from tender announcement.

        Args:
            title: Tender title
            content: Tender content

        Returns:
            TenderExtractModel with extracted data, or None if extraction fails

        Raises:
            Exception: If extraction fails after retries
        """
        try:
            # Prepare prompt
            prompt = f"""请从以下招标公告中提取关键信息:

标题: {title}

内容:
{content[:5000]}

返回JSON格式的提取结果:"""

            # Call Gemini API
            response = self.model.generate_content(prompt)

            if not response.text:
                logger.warning("Empty response from Gemini API")
                return None

            # Parse response
            extracted_data = self._parse_json_response(response.text)

            if not extracted_data:
                logger.warning(f"Failed to parse JSON from response: {response.text[:200]}")
                return None

            # Validate with Pydantic
            tender_data = TenderExtractModel(**extracted_data)

            logger.info(f"Successfully extracted data from: {title[:50]}...")
            return tender_data

        except Exception as e:
            logger.error(f"Extraction failed: {e}", exc_info=True)
            raise

    def _parse_json_response(self, text: str) -> Optional[dict]:
        """Parse JSON from AI response, handling various formats."""
        # Try direct JSON parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code block
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Try to find JSON object in text
        json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        return None


# Create singleton instance
extraction_service = ExtractionService()
