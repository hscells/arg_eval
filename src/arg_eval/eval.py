from typing import List, Dict, Type, Tuple

from arg_eval.io import Responses, Response, Truths, QuestionBank, QuestionResponse
from arg_eval.metrics import MetricMixin


def load_eval(truths: Truths, responses: Responses, questions: QuestionBank) -> Dict[str, Dict[str, List[Tuple[QuestionResponse, Response]]]]:
    # Only evaluate responses that have been answered.
    response_question_ids = list(set([x.question_id for x in responses]))
    truths_filtered = list(filter(lambda x: x.question_id in response_question_ids, truths))

    assert len(truths_filtered) == len(responses)

    struct = {}
    for question in questions:
        if question.task not in struct:
            struct[question.task] = {}
        if question.quality_property not in struct[question.task]:
            struct[question.task][question.quality_property] = []

    # Sort the responses by questions.
    # TODO this may be slow, but is okay for now.
    truths_sorted = sorted(truths_filtered, key=lambda x: (x.question_id, x.topic_id))
    responses_sorted = sorted(responses, key=lambda x: [y.question_id for y in truths_sorted].index(x.question_id))
    for question in questions:
        for truth, response in zip(truths_sorted, responses_sorted):
            assert truth.question_id == response.question_id
            assert truth.topic_id == response.topic_id
            assert isinstance(response.response, type(truth.expected_response))

            if question.question_id == truth.question_id:
                struct[question.task][question.quality_property].append((truth, response))

    return struct


def eval_agg(truths: Truths, responses: Responses, questions: QuestionBank, metrics: List[Type[MetricMixin]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    struct = load_eval(truths, responses, questions)

    # Calculate the results.
    results = {}
    for task, d in struct.items():
        results[task] = {}
        for property, pairs in d.items():
            results[task][property] = {}
            t, r = [], []
            for truth, response in pairs:
                t.append(truth)
                r.append(response)

            for metric in metrics:
                m = metric(t, r)
                results[task][property][m.__class__.__doc__] = m.agg()

    return results


def eval_ind(truths: Truths, responses: List[Response], questions: QuestionBank, metrics: List[Type[MetricMixin]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    struct = load_eval(truths, responses, questions)

    # Calculate the results.
    # Calculate the results.
    results = {}
    for task, d in struct.items():
        results[task] = {}
        for property, pairs in d.items():
            results[task][property] = {}
            t, r = [], []
            for truth, response in pairs:
                t.append(truth)
                r.append(response)

            for truth, response in zip(t, r):
                for metric in metrics:
                    m = metric(truths, responses)
                    results[task][property][f"{m.__class__.__doc__}#{truth.question_id}@{response.topic_id}"] = m.score(truth, response)

    return results
