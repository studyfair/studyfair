import argparse
import libcst as cst

import visitors.function_definition_visitor as fdv
from mutations.mSDL import mSDL


def main():
    mutations = ["mSDL"]

    parser = argparse.ArgumentParser(
        prog="mutator.py", description="Python CST-based Type-3 mutator"
    )
    parser.add_argument("input")
    parser.add_argument("-o", "--output", action="store_const")
    parser.add_argument("-m", "--mutation", choices=mutations, required=True)
    parser.add_argument("-s", "--seed", action="store_const")

    args = parser.parse_args()

    with open(args.input, "r") as source:
        data = source.read()
        source_tree = cst.parse_module(data)

        visitor = fdv.FunctionDefinitionCollector()
        source_tree.visit(visitor)

        mutator = mSDL(source_tree)
        result = mutator.call()
        if args.output:
            with open(args.output, "w") as dest:
                dest.write(result.code)
        else:
            print(result.code)


if __name__ == "__main__":
    main()
