# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

app = FastAPI(title="Business Copilot", version="1.0.0")


class Question(BaseModel):
    text: str
    business_type: str
    context: Dict[str, Any] = None


class Answer(BaseModel):
    response: str
    sources: List[str] = []
    confidence: float = 0.95


@app.get("/")
async def root():
    return {
        "message": "Business Copilot API",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@app.post("/answer")
async def get_answer(question: Question):
    # Простая логика для демонстрации
    business_responses = {
        "кафе": "Для кафе рекомендую использовать упрощенную систему налогообложения (УСН) 6%. Основные расходы: аренда, продукты, зарплата персонала. Для привлечения клиентов сделайте акцент на социальных сетях и локальной рекламе.",
        "магазин": "Для магазина оптимально использовать патентную систему налогообложения (ПСН). Важно вести учет товаров и автоматизировать кассовые операции. Для продвижения используйте контекстную рекламу и программы лояльности.",
        "услуги": "Для услуг рекомендую УСН 6%. Основные статьи расходов: реклама, инструменты/оборудование, обучение. Фокусируйтесь на реферальных программах и отзывах клиентов для привлечения новых заказов."
    }

    default_response = "Я - бизнес-ассистент для микробизнеса. Задайте конкретный вопрос о вашем бизнесе, и я дам практические рекомендации по налогам, маркетингу, управлению или финансам."

    response = business_responses.get(question.business_type.lower(), default_response)

    return Answer(
        response=response,
        sources=["База знаний Альфа-Банка", "Налоговый кодекс РФ"],
        confidence=0.85
    )


@app.get("/suggestions")
async def get_suggestions(business_type: str = "общий"):
    suggestions = {
        "кафе": [
            "Какие налоги платить для кафе?",
            "Как рассчитать точку безубыточности?",
            "Как нанять персонал для общепита?",
            "Какие разрешения нужны для открытия кафе?",
            "Как вести учет продуктов и отходов?"
        ],
        "магазин": [
            "Как выбрать систему налогообложения для магазина?",
            "Как вести кассовую дисциплину?",
            "Как автоматизировать учет товаров?",
            "Как привлечь покупателей в офлайн-магазин?",
            "Какие документы нужны для торговли?"
        ],
        "услуги": [
            "Как составить договор с клиентом?",
            "Какие налоги для ИП оказывающего услуги?",
            "Как страховать профессиональные риски?",
            "Как вести документооборот для услуг?",
            "Как масштабировать бизнес услуг?"
        ]
    }

    return {"suggestions": suggestions.get(business_type.lower(), suggestions["общий"])}