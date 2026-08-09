from dataclasses import dataclass


@dataclass(frozen=True)
class SentimentReading:
    asset: str
    score: float
    label: str
    source: str
    detail: str = ""

    @property
    def emoji(self) -> str:
        normalized = self.label.lower().replace("_", " ")
        if "extreme fear" in normalized:
            return "😱"
        if "fear" in normalized:
            return "😰"
        if "extreme greed" in normalized:
            return "🤑"
        if "greed" in normalized:
            return "😊"
        return "😐"
