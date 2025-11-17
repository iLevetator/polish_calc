"""
Модуль test_calculator содержит тесты для калькулятора.
"""
import unittest

from main import PolishCalculator


class TestCalculator(unittest.TestCase):
    """Tests for RPD calculator"""
    calc = PolishCalculator()

    def test_simple_addition(self):
        """Simple addition"""
        res = self.calc.evaluate("2 + 3")
        self.assertAlmostEqual(5.0, res, delta=0.001, msg=f"Expected: 5.0, got: {res}")

    def test_subtraction_with_parentheses(self):
        """Subtraction and parentheses"""
        res = self.calc.evaluate("(5 - 3) + (1 - 2)")
        self.assertAlmostEqual(1.0, res, delta=0.001, msg=f"Expected: 1.0, got: {res}")

    def test_multiplication_precedence(self):
        """Multiplication and division precedence"""
        res = self.calc.evaluate("2 + 3 * 4")
        self.assertAlmostEqual(14.0, res, delta=0.001, msg=f"Expected: 14.0, got: {res}")

    def test_division_precedence(self):
        """Division left-associativity"""
        res = self.calc.evaluate("8 / 4 / 2")
        self.assertAlmostEqual(1.0, res, delta=0.001, msg=f"Expected: 1.0, got: {res}")

    def test_exponentiation(self):
        """Exponentiation (right-associative)"""
        res = self.calc.evaluate("2 ^ 3 ^ 2")
        self.assertAlmostEqual(512.0, res, delta=0.001, msg=f"Expected: 512.0, got: {res}")

    def test_complex_expression(self):
        """Complex expression"""
        res = self.calc.evaluate("3 + 5 * (2 + 4) - 2")
        self.assertAlmostEqual(31.0, res, delta=0.001, msg=f"Expected: 31.0, got: {res}")

    def test_division_by_zero(self):
        """Division by zero throws exception"""
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("1 / 0")

    def test_mismatched_parentheses(self):
        """Mismatched parentheses"""
        with self.assertRaises(ValueError) as context:
            self.calc.evaluate("2 + (3")
        self.assertIn("Mismatched parentheses", str(context.exception))

    def test_rpn_addition(self):
        """RPN: simple addition"""
        rpn = self.calc.to_reverse_polish_notation("2 + 3")
        expected = "2 3 +"
        self.assertEqual(expected, rpn, f"Expected {expected}, got: {rpn}")

    def test_rpn_precedence(self):
        """RPN: multiply before add"""
        rpn = self.calc.to_reverse_polish_notation("2 + 3 * 4")
        expected = "2 3 4 * +"
        self.assertEqual(expected, rpn, f"Expected {expected}, got: {rpn}")

    def test_rpn_parentheses(self):
        """RPN: parentheses change order"""
        rpn = self.calc.to_reverse_polish_notation("(2 + 3) * 4")
        expected = "2 3 + 4 *"
        self.assertEqual(expected, rpn, f"Expected {expected}, got: {rpn}")

    def test_empty_expression(self):
        """Empty input"""
        with self.assertRaises(ValueError):
            self.calc.evaluate("")

    def test_single_number(self):
        """One number"""
        rpn = self.calc.evaluate("7")
        expected = 7
        self.assertEqual(expected, rpn, f"Expected {expected}, got: {rpn}")

    def test_with_wrong_arguments(self):
        """Wrong arguments"""
        with self.assertRaises(ValueError):
            self.calc.evaluate("a b +")


if __name__ == '__main__':
    unittest.main()
