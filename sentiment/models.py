from dataclasses import dataclass


@dataclass(frozen=True)
class SentimentReading:
    asset: str
    score: float
    label: str
    source: str
    metrics: tuple[str, ...] = ()
