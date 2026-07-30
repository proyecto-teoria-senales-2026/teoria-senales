"""Pruebas del explorador visual de señales."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.signal_processing.explorer import explore_signals


class SignalExplorerTests(unittest.TestCase):
    def test_reports_circular_overlap_when_n_is_insufficient(self) -> None:
        exploration = explore_signals("1, 2, 1", "1, -1, 2", 3)

        self.assertTrue(exploration.has_circular_overlap)
        self.assertEqual(exploration.minimum_length, 5)
        np.testing.assert_allclose(
            exploration.frequency_result,
            [4, 3, 1],
        )

    def test_preserves_linear_convolution_with_sufficient_n(self) -> None:
        exploration = explore_signals("1, 2, 1", "1, -1, 2", 5)

        self.assertFalse(exploration.has_circular_overlap)
        np.testing.assert_allclose(
            exploration.frequency_result,
            exploration.linear_result,
        )

    def test_rejects_sequences_outside_the_exploration_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "entre 2 y 8"):
            explore_signals("1", "1, 2", 2)

    def test_rejects_n_shorter_than_an_input_signal(self) -> None:
        with self.assertRaisesRegex(ValueError, "mayor o igual que 4"):
            explore_signals("1, 2, 3, 4", "1, 2", 3)


if __name__ == "__main__":
    unittest.main()
