"""Archive task: Unit Tests For Edge Cases.

Generated for 2020-12-17. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

import unittest


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class EdgeCaseTests(unittest.TestCase):
    def test_clamps_below_range(self):
        self.assertEqual(clamp(-4, 0, 10), 0)

    def test_clamps_above_range(self):
        self.assertEqual(clamp(18, 0, 10), 10)


if __name__ == "__main__":
    unittest.main()
