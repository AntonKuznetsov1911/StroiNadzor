"""
Сервис для работы с ИИ (OpenAI/Claude)
"""
from typing import Optional, List
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Сервис для работы с ИИ консультантом"""

    def __init__(self):
        self.openai_client = None
        self.claude_client = None

        # Инициализация клиентов если есть API ключи
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("OpenAI library not installed")

        if settings.CLAUDE_API_KEY:
            try:
                import anthropic
                self.claude_client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
                logger.info("Claude client initialized")
            except ImportError:
                logger.warning("Anthropic library not installed")

    def ask_question(
        self,
        question: str,
        context: Optional[str] = None,
        regulations: Optional[List[dict]] = None
    ) -> dict:
        """
        Задать вопрос ИИ консультанту

        Args:
            question: Вопрос пользователя
            context: Контекст проекта/этапа
            regulations: Список релевантных нормативов

        Returns:
            dict с ответом и ссылками на нормативы
        """
        # Формирование контекста
        system_prompt = """Ты - эксперт по строительным нормативам России.
Твоя задача - помогать инженерам и техническим специалистам с вопросами
о строительных нормах, правилах и технических регламентах.

Отвечай конкретно, со ссылками на нормативы.
"""

        regulations_context = ""
        if regulations:
            regulations_context = "\n\nДоступные нормативы:\n"
            regulations_context += "\n".join([
                f"- {reg['code']}: {reg['title']}"
                for reg in regulations
            ])

        user_context = f"\nКонтекст проекта: {context}" if context else ""

        full_prompt = f"{system_prompt}{regulations_context}{user_context}\n\nВопрос: {question}"

        try:
            # Приоритет Claude API
            if self.claude_client:
                return self._ask_claude(full_prompt)
            elif self.openai_client:
                return self._ask_openai(full_prompt)
            else:
                # Заглушка если нет API
                return {
                    "answer": f"Это демо-ответ. Для вопроса '{question}' рекомендуем обратиться к следующим нормативам: {', '.join([r['code'] for r in regulations[:3]])}",
                    "referenced_regulations": [r['code'] for r in regulations[:3]] if regulations else [],
                    "confidence": 0.5
                }

        except Exception as e:
            logger.error(f"Error asking AI: {str(e)}")
            raise

    def _ask_claude(self, prompt: str) -> dict:
        """Запрос к Claude API"""
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.content[0].text

        return {
            "answer": answer,
            "referenced_regulations": self._extract_regulations(answer),
            "confidence": 0.85
        }

    def _ask_openai(self, prompt: str) -> dict:
        """Запрос к OpenAI API"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты - эксперт по строительным нормативам России."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "referenced_regulations": self._extract_regulations(answer),
            "confidence": 0.85
        }

    def _extract_regulations(self, text: str) -> List[str]:
        """Извлечение кодов нормативов из текста"""
        import re

        # Паттерны для СП, ГОСТ и т.д.
        patterns = [
            r'СП\s+\d+\.[\d\.]+',
            r'ГОСТ\s+\d+[\-\d]*',
            r'СанПиН\s+[\d\.]+',
        ]

        regulations = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            regulations.extend(matches)

        return list(set(regulations))  # Уникальные значения


# Singleton instance
ai_service = AIService()
