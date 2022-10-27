from abc import ABC, abstractmethod

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
