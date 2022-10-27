from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Question:
    question_id: str
    parent_question: str
    quality_property: str
    task: str
    question: str


@dataclass_json
@dataclass
class Response:
    topic_id: str
    question_id: str
    response: Union[str, float]


@dataclass_json
@dataclass
class QuestionResponse:
    question_id: str
    topic_id: str
    expected_response: Union[str, float]
    rational: str


QuestionBank = List[Question]
Responses = List[Response]
Truths = List[QuestionResponse]


def load_questions(fname: Union[str, Path]) -> QuestionBank:
    if not isinstance(fname, Path):
        fname = Path(fname)
    assert fname.is_file()
    questions = []
    with open(fname, "r") as f:
        for line in f:
            questions.append(Question.from_json(line))
    return questions


def load_responses(fname: Union[str, Path]) -> Responses:
    if not isinstance(fname, Path):
        fname = Path(fname)
    assert fname.is_file()
    responses = []
    with open(fname, "r") as f:
        for line in f:
            responses.append(Response.from_json(line))
    return responses


def load_truths(fname: Union[str, Path]) -> Truths:
    if not isinstance(fname, Path):
        fname = Path(fname)
    assert fname.is_file()
    truths = []
    with open(fname, "r") as f:
        for line in f:
            truths.append(QuestionResponse.from_json(line))
    return truths
