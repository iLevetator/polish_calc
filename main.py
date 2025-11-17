"""
Модуль main - точка входа в калькулятор.
Предоставляет интерфейс командной строки для вычисления математических выражений.
"""

class PolishCalculator:
    """ Calculator bases on reverse polish notation """

    PRIORITY = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    OPERATORS = {'+', '-', '*', '/', '^'}

    def evaluate(self, expression: str) -> float:
        """Evaluate expression and return result"""
        tokens = self.tokenize(expression)
        rpn = self.to_rpn(tokens)
        return self.evaluate_rpn(rpn)

    @staticmethod
    def tokenize(expression: str):
        """Tokenize expression"""
        tokens, current_number = [], []
        for char in expression:
            if char.isspace():
                continue
            if char.isdigit() or char == '.':
                current_number.append(char)
            else:
                if current_number:
                    tokens.append(''.join(current_number))
                    current_number = []
                tokens.append(char)
        if current_number:
            tokens.append(''.join(current_number))
        return tokens

    def to_rpn(self, tokens: list):
        """Convert tokens to RPN"""
        output, operators = [], []
        for token in tokens:
            if self.is_number(token):
                output.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if not operators:
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Remove '('
            elif token in self.OPERATORS:
                while (operators and
                       operators[-1] != '(' and
                       (self.PRIORITY[operators[-1]] > self.PRIORITY[token] or
                        (self.PRIORITY[operators[-1]] == self.PRIORITY[token] and token != '^'))):
                    output.append(operators.pop())
                operators.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")
        while operators:
            op = operators.pop()
            if op in '()':
                raise ValueError("Mismatched parentheses")
            output.append(op)
        return output

    @staticmethod
    def is_number(token: str) -> bool:
        """Check if token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def evaluate_rpn(self, rpn: list) -> float:
        """Evaluate rpn and return result"""
        stack = []
        for token in rpn:
            if self.is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid RPN expression")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                elif token == '^':
                    result = pow(a, b)
                else:
                    raise ValueError(f"Unknown operator: {token}")
                stack.append(result)
        if len(stack) != 1:
            raise ValueError("Invalid RPN expression")
        return stack.pop()

    def to_reverse_polish_notation(self, expression: str):
        """Convert expression to reverse polish notation"""
        tokens = self.tokenize(expression)
        return ' '.join(self.to_rpn(tokens))


def main():
    """Main function"""
    calc = PolishCalculator()
    expression = input("Enter expression: ")
    # expression = "3 + 4 * 2 / (1 - 5) ^ 2"
    # print(f"Enter expression: {expression}")
    print(f"Polish notation: {calc.to_reverse_polish_notation(expression)}")
    print(f"Result: {calc.evaluate(expression)}")

if __name__ == '__main__':
    main()
