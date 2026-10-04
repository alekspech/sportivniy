from dataclasses import dataclass, field as dc_field
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import uuid4
import random


class Field(Enum): # перечисление предметов. (питон математика физика)
    PYTHON = "python"
    DEFAULT = "def"
    GEOMETRY = 'geometry'


class QuestionType(Enum):
    CHOICE = "choice"
    TEXT = "text"
    MATCH = "match"


def _new_id() -> str:
    return str(uuid4())


@dataclass#(slots=True)
class Answer:
    id: str = dc_field(default_factory=_new_id)
    data: str = ""
    is_true: bool = False
    img_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "data": self.data,
            "is_true": int(self.is_true),
        }
        if self.img_path is not None:
            d["img_path"] = self.img_path
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Answer":
        return Answer(
            id=d["id"],
            data=d["data"],
            is_true=bool(d["is_true"]),
            img_path=d.get("img_path"),
        )


@dataclass#(slots=True)
class Question:
    id: str = dc_field(default_factory=_new_id)
    field: Field = Field.DEFAULT
    topic: str = "python"
    task: str = ""
    question_type: QuestionType = QuestionType.CHOICE
    answers_set: List[Answer] = dc_field(default_factory=list)
    img_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "field": self.field.value,
            "topic": self.topic,
            "task": self.task,
            "question_type": self.question_type.value,
            "answers_set": [a.to_dict() for a in self.answers_set],
        }
        if self.img_path is not None:
            d["img_path"] = self.img_path
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Question":
        answers = [Answer.from_dict(ad) for ad in d["answers_set"]]
        random.shuffle(answers)
        return Question(
            id=d["id"],
            field=Field(d["field"]),
            topic=d["topic"],
            task=d["task"],
            question_type=QuestionType(d["question_type"]),
            answers_set=answers,
            img_path=d.get("img_path"),
        )

if __name__ == '__main__':
    q = Question(
    task="Что делает функция print()?",
    topic="core",
    answers_set=[
        Answer(data="Выводит текст в консоль", is_true=True),
        Answer(data="Сохраняет файл", is_true=False),
        ]
    )

    json_data = q.to_dict()
