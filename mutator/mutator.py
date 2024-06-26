import argparse
import sys
import random
import enum
import json

from dataclasses import dataclass
from contextlib import nullcontext

import libcst

from mutations.registry import Registry as MutationsRegistry
from mutations.injection_trace import InjectionTrace
from mutations.base import Base
from mutations.mSDL import mSDL
from mutations.mDL import mDL
from mutations.mSIL import mSIL
from mutations.mRLN import mRLN
from mutations.mRLS import mRLS
from mutations.mIL import mIL


@dataclass
class MutationSpec:
    name: str
    lower_bound: int = 1
    upper_bound: int = 1


class Distribution(enum.Enum):
    UNIFORM = "uniform"

    def __str__(self) -> str:
        return self.value


def main():
    args = _parse_arguments()
    randomizer = random.Random(args.seed)
    injection_trace = InjectionTrace()

    with open(args.input, "r") as source:
        data = source.read()
        source_tree = libcst.parse_module(data)

        result = source_tree
        for mutation_spec in args.mutations:
            order = randomizer.randint(
                mutation_spec.lower_bound, mutation_spec.upper_bound
            )
            for _ in range(order):
                result = _apply_mutation(
                    mutation_spec.name, result, randomizer, injection_trace
                )

    _output_result(result, args.output)

    if args.injection_trace is not None:
        with open(args.injection_trace, "w") as file:
            file.write(json.dumps(injection_trace.serializable_list()))


def _apply_mutation(
    name: str,
    source_tree: libcst.Module,
    randomizer: random.Random,
    injection_trace: InjectionTrace,
):
    mutator: Base

    match name:
        case MutationsRegistry.M_SDL.value:
            mutator = mSDL(source_tree, randomizer, injection_trace)
        case MutationsRegistry.M_DL.value:
            mutator = mDL(source_tree, randomizer, injection_trace)
        case MutationsRegistry.M_SIL.value:
            mutator = mSIL(source_tree, randomizer, injection_trace)
        case MutationsRegistry.M_RLN.value:
            mutator = mRLN(source_tree, randomizer, injection_trace)
        case MutationsRegistry.M_RLS.value:
            mutator = mRLS(source_tree, randomizer, injection_trace)
        case MutationsRegistry.M_IL.value:
            mutator = mIL(source_tree, randomizer, injection_trace)
        case "any":
            mutator = randomizer.choice([mSDL, mDL, mSIL, mRLN, mRLS, mIL])(
                source_tree, randomizer, injection_trace
            )
        case _:
            raise NotImplementedError(f"Unknown mutation operator name: `{name}`")

    return mutator.call()


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog="mutator.py", description="Python CST-based code mutation framework"
    )
    parser.add_argument("input")
    parser.add_argument("-o", "--output", action="store")
    parser.add_argument("-m", "--mutations", action="store", required=True)
    parser.add_argument("-s", "--seed", action="store", type=int)
    parser.add_argument("-t", "--injection-trace", action="store", type=str)
    parser.add_argument(
        "-d",
        "--distribution",
        action="store",
        type=Distribution,
        choices=list(Distribution),
        default=Distribution.UNIFORM,
    )

    args = parser.parse_args()
    args.mutations = _parse_mutations_argument(args.mutations)
    if args.seed is None:
        args.seed = random.randint(0, 1000)

    return args


def _parse_mutations_argument(raw_input: str):
    mutations = []

    chunks = raw_input.split(",")
    for chunk in chunks:
        if ":" in chunk:
            name, order = chunk.split(":")
            if "-" in order:
                lower_bound, upper_bound = order.split("-")
                mutations.append(MutationSpec(name, int(lower_bound), int(upper_bound)))
            else:
                mutations.append(MutationSpec(name, int(order), int(order)))
        else:
            mutations.append(MutationSpec(chunk))

    return mutations


def _output_result(result, output, fallback_file=sys.stdout):
    with open(output, "w") if output else nullcontext(fallback_file) as dest:
        dest.write(result.code)


if __name__ == "__main__":
    main()
