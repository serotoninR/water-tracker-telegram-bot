from pydantic import BaseModel, field_validator


class WeightInput(BaseModel):
    weight: int

    @field_validator("weight", mode="before")
    @classmethod
    def check_weight(cls, v: object) -> int:
        # Если пришла строка, проверяем, состоит ли она только из цифр
        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError("Это не цифры!")
            v = int(v)

        if not isinstance(v, (int, float)):
            raise ValueError("Это не цифры!")

        if isinstance(v, float) and not v.is_integer():
            raise ValueError("Вес должен быть целым числом")

        v_int = int(v)

        if v_int < 20:
            raise ValueError("Вес должен быть больше 20 кг")
        if v_int > 320:
            raise ValueError("Вес должен быть меньше 320 кг")

        return v_int


class WaterAmountInput(BaseModel):
    amount: int

    @field_validator("amount", mode="before")
    @classmethod
    def check_amount(cls, v: object) -> int:
        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError("Введи целое число мл!")
            v = int(v)

        if not isinstance(v, (int, float)):
            raise ValueError("Введи целое число мл!")

        v_int = int(v)

        if v_int < 1:
            raise ValueError("Минимум 1 мл")
        if v_int > 1000:
            raise ValueError("Максимум 1000 мл")

        return v_int


class ProgressResponse(BaseModel):
    user_id: int
    daily_norm: int | None = None
    today_amount: int = 0
    progress_percent: float = 0.0
    scale: str = "[░░░░░░░░░░]"

    @field_validator("progress_percent")
    @classmethod
    def clamp_percent(cls, v: float) -> float:
        return min(v, 100.0)
