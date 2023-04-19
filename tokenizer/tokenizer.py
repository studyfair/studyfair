import argparse
import json
import io
import tokenize


def extract_tokens(source: str):
   fn_filter = lambda item: item and len(item) > 0
   fn_mapper = lambda item: str(item[1]).strip()

   return list(
      filter(fn_filter, map(fn_mapper, tokenize.generate_tokens(io.StringIO(source).readline)))
   )


def main():
    parser = argparse.ArgumentParser(
        prog="tokenizer.py", description="Tokenizer"
    )
    parser.add_argument("input")

    args = parser.parse_args()

    with open(args.input, "r") as source:
      data = source.read()
      data = json.loads(data)

      for datum in data:
         value = datum["item"]
         tokens_spec = extract_tokens(value)
         print(json.dumps(tokens_spec))


if __name__ == "__main__":
    main()