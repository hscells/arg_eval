from abc import ABC, abstractmethod
from rouge_score import rouge_scorer

from arg_eval.io import Truths, Responses, Response, QuestionResponse


class MetricMixin(ABC):
    def __init__(self, truths: Truths, responses: Responses):
        self.truths = truths
        self.responses = responses

    @abstractmethod
    def score(self, truth: QuestionResponse, response: Response) -> float:
        raise NotImplementedError()

    @abstractmethod
    def agg(self) -> float:
        raise NotImplementedError()


class NumericalMetricMixin(MetricMixin):

    @abstractmethod
    def score(self, truth: QuestionResponse, response: Response) -> float:
        pass

    @abstractmethod
    def agg(self) -> float:
        pass


class StringMetricMixin(MetricMixin):
    @abstractmethod
    def score(self, truth: QuestionResponse, response: Response) -> float:
        pass

    @abstractmethod
    def agg(self) -> float:
        pass


class Accuracy(MetricMixin):
    """acc"""

    def score(self, truth: QuestionResponse, response: Response) -> float:
        if truth.expected_response == response.response:
            return 1
        return 0

    def agg(self) -> float:
        num_correct = 0.0
        for truth, response in zip(self.truths, self.responses):
            num_correct += self.score(truth, response)
        return num_correct / len(self.truths)


class RougeL(StringMetricMixin):
    """rouge-l"""

    def score(self, truth: QuestionResponse, response: Response) -> float:
        if not isinstance(truth.expected_response, str):
            return 0.0
        score = rouge_scorer.RougeScorer(["rougeL"]).score(truth.expected_response, response.response)
        return score["rougeL"].fmeasure

    def agg(self) -> float:
        score = 0.0
        for truth, response in zip(self.truths, self.responses):
            score += self.score(truth, response)
        return score / len(self.truths)


class NumTopics(MetricMixin):
    """num_topics"""

    def score(self, truth: QuestionResponse, response: Response) -> float:
        return 1

    def agg(self) -> float:
        return len(set([x.topic_id for x in self.responses]))


class NumQuestions(MetricMixin):
    """num_questions"""

    def score(self, truth: QuestionResponse, response: Response) -> float:
        return 1

    def agg(self) -> float:
        return len(set([x.question_id for x in self.responses]))
