#!/usr/bin/env python
math_tokens = "+-*/"
single_char_tokens = f"(){math_tokens}"


def tokenize(string):
    tokens = []
    current_token = ""

    for index, char in enumerate(string):

        if not char.isnumeric() and len(current_token) > 0:
            tokens.append(current_token)
            current_token = ""

        if char in single_char_tokens:
            tokens.append(char)
        elif char.isnumeric():
            current_token += char
        elif char == " ":
            pass
        else:
            print(f"[!] unknown char '{char}' at {index}")

    if current_token:
        tokens.append(current_token)
        current_token = ""

    return tokens


def parse(tokens):
    stack = []
    running = True

    while running:
        try:
            token = next(tokens)
            if token == "(":
                stack.append(parse(tokens))
            elif token.isnumeric():
                if len(stack) == 0:
                    print(
                        f"[!] unexpected number token {token}, no operator!\n{str(list(tokens))}\n"
                    )
                stack.append(token)
            elif token in math_tokens:
                stack.append(token)
            elif token == ")":
                running = False
        except StopIteration:
            running = False

    return stack


def evaluate_expression(expression):

    if len(expression) == 0:
        return []
    if type(expression) is not list:
        raise Exception(f"unexpected expression: {expression}")

    values = []
    first = expression.pop(0)

    if type(first) is list:
        return evaluate(first)

    elif first in math_tokens:

        operator = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }[first]

        values = []
        for value in expression:
            if type(value) is str and value.isnumeric():
                values.append(int(value))
            if type(value) is list:
                values.append(evaluate_expression(value))

        final = 0 if first in "+-" else 1
        for value in values:
            final = operator(final, value)
        return final

    else:
        raise Exception(f"unexpected first {first} {type(first)}, {expression}")

    return values


def evaluate(expressions):
    return [evaluate_expression(expr) for expr in expressions]


def main():
    f = lambda s: evaluate(parse(iter(tokenize(s))))
    while 1:
        line = input("$ ")
        try:
            print(f(line))
        except Exception as e:
            print(e)


import unittest


class Test(unittest.TestCase):
    def test_evaluate(self):
        f = lambda s: evaluate(parse(iter(tokenize(s))))
        self.assertEqual(f(""), [])
        self.assertEqual(f("(+ 1 1)"), [2])
        self.assertEqual(f("(+ 1 1) (+ 1 1)"), [2, 2])
        self.assertEqual(f("(+ (+ 1 1) (+ 1 1)) (+ (+ 1 1) (+ 1 1))"), [4, 4])


if __name__ == "__main__":
    main()
