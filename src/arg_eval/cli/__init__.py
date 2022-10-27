from pathlib import Path

import click

import arg_eval
import arg_eval.io as io
from arg_eval.eval import eval_agg, eval_ind
from arg_eval.metrics import Accuracy, NumTopics, NumQuestions, RougeL

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
DEFAULT_AGG_METRICS = [NumTopics, NumQuestions, Accuracy, RougeL]
DEFAULT_IND_METRICS = [Accuracy, RougeL]


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=arg_eval.__version__)
@click.argument(
    "truths_file",
    type=click.Path(),
    required=True,
)
@click.argument(
    "questions_file",
    type=click.Path(),
    required=True,
)
@click.argument(
    "responses_file",
    type=click.Path(),
    required=True,
)
@click.option('--agg/--ind', default=True)
def cli(truths_file: Path, questions_file: Path, responses_file: Path, agg: bool):
    """evaluation"""
    truths = io.load_truths(truths_file)
    questions = io.load_questions(questions_file)
    responses = io.load_responses(responses_file)

    if not agg:
        for task, a in eval_ind(truths, responses, questions, DEFAULT_IND_METRICS).items():
            for prop, b in a.items():
                print(f"{task}#{prop}")
                for k, v in b.items():
                    print(f"{k}\t{v}")

    for task, a in eval_agg(truths, responses, questions, DEFAULT_AGG_METRICS).items():
        for prop, b in a.items():
            print(f"{task}#{prop}")
            for k, v in b.items():
                print(f"{k}\t{v}")
