from typing import Optional

from pydantic import BaseModel, field_validator


class WeightInput(BaseModel):
    # Схема ввода веса
    weight: float | str

    @field_validator("weight")
    @classmethod
    def check_weight(cls, v: float | str) -> int:
        if isinstance(v, str):
            raise ValueError("Это не цифры!")
        if v < 20:
            raise ValueError("Вес должен быть больше 20 кг")
        if v > 320:
            raise ValueError("Вес должен быть меньше 320 кг")
        if not v.is_integer():
            raise ValueError("Вес должен быть целым числом")
        return int(v)


class WaterAmountInput(BaseModel):
    # Схема для ввода воды
    amount: int

    @field_validator("amount")
    @classmethod
    def check_amount(cls, v: int | str) -> int:
        if v < 1:
            raise ValueError("Минимум 1 мл")
        if v > 1000:
            raise ValueError("Максимум 1000 мл")
        return v


class ProgressResponse(BaseModel):
    # Схема для ответа с прогрессом
    user_id: int
    daily_norm: Optional[int] = None
    today_amount: int = 0
    progress_percent: float = 0.0
    scale: str = "[░░░░░░░░░░]"

    @field_validator("progress_percent")
    @classmethod
    def clamp_percent(cls, v: float) -> float:
        # Ограничение процентов до 100
        return min(v, 100.0)
