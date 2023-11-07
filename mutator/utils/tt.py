import split_module
import tokenizer
import argparse

from pathlib import Path


def call_splitter(dir: str, output: str, repository: str, revision: str):
    result = []
    files = list(Path(dir).rglob("*.py"))

    for file in files:
        result = result + split_module.split(file, repository, revision)

    return result


def call_tokenizer(data, output):
    return tokenizer.tokenize_data(data, output)


def main():
    parser = argparse.ArgumentParser(prog="tt.py")

    parser.add_argument("dir")
    parser.add_argument("--output")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()

    if args.output is None or len(args.output) == 0:
        args.output = args.dir + "/result.json"

    result = call_splitter(args.dir, None, args.repository, args.revision)
    call_tokenizer(result, args.output)


if __name__ == "__main__":
    main()
