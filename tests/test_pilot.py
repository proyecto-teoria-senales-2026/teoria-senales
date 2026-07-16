"""Pruebas del núcleo numérico y del seguimiento del piloto."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.pilot_cli import run_demo
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
from teoria_senales.signal_processing.convolution import (
    frequency_domain_convolution,
    linear_convolution,
    minimum_transform_length,
)


class ConvolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.exercise = ConvolutionPilot()

    def test_approved_reference_values(self) -> None:
        self.assertEqual(linear_convolution(self.exercise.x, self.exercise.h).tolist(), [1, 1, 1, 3, 2])
        self.assertEqual(
            frequency_domain_convolution(self.exercise.x, self.exercise.h, 3).round(10).tolist(),
            [4, 3, 1],
        )
        self.assertEqual(
            frequency_domain_convolution(self.exercise.x, self.exercise.h, 5).round(10).tolist(),
            [1, 1, 1, 3, 2],
        )
        self.assertEqual(minimum_transform_length(self.exercise.x, self.exercise.h), 5)

    def test_validations_reject_incorrect_lengths(self) -> None:
        self.assertFalse(self.exercise.validate("paso_1", [3, 3, 4]))
        self.assertFalse(self.exercise.validate("paso_1", [3.2, 3, 5]))
        self.assertTrue(self.exercise.validate("paso_1", [3, 3, 5]))

    def test_demo_generates_structured_session_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            json_path, pdf_path = run_demo(temporary_directory)
            self.assertTrue(json_path.exists())
            self.assertTrue(pdf_path.exists())
            self.assertGreater(pdf_path.stat().st_size, 5_000)


if __name__ == "__main__":
    unittest.main()
