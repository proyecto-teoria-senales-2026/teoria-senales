import math
import unittest

import numpy as np

from teoria_senales.signal_processing.convolution import (
    frequency_domain_convolution,
    linear_convolution,
    minimum_transform_length,
    parse_numeric_sequence,
    values_match,
)
from teoria_senales.signal_processing.fourier_reconstruction import (
    exact_mean_square_error,
    gibbs_overshoot_ratio,
    reconstruct_rectangular_pulse,
    rectangular_periodic_signal,
)
from teoria_senales.signal_processing.fourier_series import (
    harmonic_amplitude_phase,
    rectangular_pulse_coefficients,
    reconstruct_trigonometric_series,
)
from teoria_senales.signal_processing.fundamental_signals import (
    FundamentalSignalKind,
    discrete_indices,
    generate_fundamental_signal,
    sinusoidal_period_samples,
)
from teoria_senales.signal_processing.signal_characteristics import (
    is_even_sequence,
    is_odd_sequence,
    periodic_average_power,
    signal_energy,
)


class FundamentalSignalsTests(unittest.TestCase):
    def test_indices_are_inclusive(self):
        np.testing.assert_array_equal(discrete_indices(-2, 2), [-2, -1, 0, 1, 2])

    def test_invalid_index_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            discrete_indices(2, -2)

    def test_impulse(self):
        signal = generate_fundamental_signal(FundamentalSignalKind.IMPULSE, -2, 2)
        np.testing.assert_array_equal(signal.samples, [0, 0, 1, 0, 0])

    def test_step(self):
        signal = generate_fundamental_signal(FundamentalSignalKind.STEP, -2, 2)
        np.testing.assert_array_equal(signal.samples, [0, 0, 1, 1, 1])

    def test_ramp(self):
        signal = generate_fundamental_signal(FundamentalSignalKind.RAMP, -2, 2)
        np.testing.assert_array_equal(signal.samples, [0, 0, 0, 1, 2])

    def test_causal_exponential(self):
        signal = generate_fundamental_signal(
            FundamentalSignalKind.EXPONENTIAL, -1, 2, exponential_base=0.5, causal=True
        )
        np.testing.assert_allclose(signal.samples, [0, 1, 0.5, 0.25])

    def test_sinusoidal_period(self):
        self.assertEqual(sinusoidal_period_samples(math.pi / 2), 4)


class SignalCharacteristicsTests(unittest.TestCase):
    def test_even_sequence(self):
        self.assertTrue(is_even_sequence([1, 2, 3, 2, 1]))

    def test_odd_sequence(self):
        self.assertTrue(is_odd_sequence([-2, -1, 0, 1, 2]))

    def test_energy(self):
        self.assertEqual(signal_energy([1, 2, 2]), 9.0)

    def test_periodic_power(self):
        self.assertEqual(periodic_average_power([1, -1, 1, -1]), 1.0)


class FourierTests(unittest.TestCase):
    def test_rectangular_coefficients(self):
        a0, an, bn = rectangular_pulse_coefficients(5)
        self.assertAlmostEqual(a0, 1.0)
        np.testing.assert_allclose(an, [2 / math.pi, 0, -2 / (3 * math.pi), 0, 2 / (5 * math.pi)])
        np.testing.assert_array_equal(bn, np.zeros(5))

    def test_amplitude_and_phase(self):
        amplitudes, phases = harmonic_amplitude_phase([1, -1], [0, 0])
        np.testing.assert_allclose(amplitudes, [1, 1])
        np.testing.assert_allclose(phases, [0, math.pi])

    def test_reconstruction_at_zero(self):
        a0, an, bn = rectangular_pulse_coefficients(5)
        value = reconstruct_trigonometric_series([0], a0, an, bn, omega_0=1)
        self.assertGreater(value[0], 0.9)

    def test_signal_uses_half_value_at_jump(self):
        np.testing.assert_allclose(rectangular_periodic_signal([-math.pi / 2, 0, math.pi / 2]), [0.5, 1, 0.5])

    def test_reconstruction_shape(self):
        time = np.linspace(-math.pi, math.pi, 101)
        self.assertEqual(reconstruct_rectangular_pulse(time, 15).shape, time.shape)

    def test_error_decreases_with_harmonics(self):
        self.assertGreater(exact_mean_square_error(1), exact_mean_square_error(15))

    def test_gibbs_reference(self):
        self.assertAlmostEqual(gibbs_overshoot_ratio(10001), 0.08949, places=4)


class ConvolutionTests(unittest.TestCase):
    def setUp(self):
        self.x = [1, 1, 1]
        self.h = [1, 2, 1]

    def test_linear_convolution(self):
        np.testing.assert_allclose(linear_convolution(self.x, self.h), [1, 3, 4, 3, 1])

    def test_minimum_transform_length(self):
        self.assertEqual(minimum_transform_length(self.x, self.h), 5)

    def test_frequency_result_matches_when_length_is_sufficient(self):
        np.testing.assert_allclose(
            frequency_domain_convolution(self.x, self.h, 5),
            linear_convolution(self.x, self.h),
            atol=1e-9,
        )

    def test_short_transform_is_rejected(self):
        with self.assertRaises(ValueError):
            frequency_domain_convolution(self.x, self.h, 2)

    def test_sequence_parser(self):
        np.testing.assert_allclose(parse_numeric_sequence("[1, 2; 3]"), [1, 2, 3])

    def test_value_matching(self):
        self.assertTrue(values_match("1 3 4 3 1", [1, 3, 4, 3, 1]))


if __name__ == "__main__":
    unittest.main()
