import argparse
import json
import io
import tokenize

def substitue_function_invokations(tokens):
   prev_token = None
   is_function: bool = False
   function_index: int = -1

   for i, token in enumerate(tokens):
      if token == "(" and prev_token == "NAME":
         is_function = True
         function_index = i - 1
      elif token == ")" and is_function:
         is_function = False
         tokens[function_index] = "FNINVOK"

      prev_token = token

def filter_token(token: str) -> str:
   return token and len(token.strip()) > 0

def transform_token(token_info: tokenize.TokenInfo) -> str:
   if token_info[0] == tokenize.NAME:
     return tokenize.tok_name[token_info[0]]

   return token_info[1]

def extract_tokens(source: str):
   impl = lambda item: transform_token(item)
   gen = tokenize.generate_tokens(io.StringIO(source).readline)

   tokens = list(filter(filter_token, map(transform_token, gen)))
   substitue_function_invokations(tokens)


   return tokens


def main():
    parser = argparse.ArgumentParser(
        prog="tokenizer.py", description="Tokenizer"
    )
    parser.add_argument("input")

    args = parser.parse_args()

    result = []
    with open(args.input, "r") as source:
      data = source.read()
      data = json.loads(data)

      for datum in data:
         tokens_spec = extract_tokens(datum["item"])
         result.append({ "tokens": tokens_spec, "identifier": datum["identifier"] })

      print(json.dumps(result))


if __name__ == "__main__":
    main()
