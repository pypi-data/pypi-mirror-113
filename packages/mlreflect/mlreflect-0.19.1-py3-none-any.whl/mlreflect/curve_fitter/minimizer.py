import numpy as np
from scipy.optimize import minimize


def q_shift_variants(q_values_prediction, q_values_input, corrected_reflectivity, n_variants, scale=0.001):
    shift = np.random.normal(loc=0, size=n_variants, scale=scale).reshape(n_variants, 1)
    shifted_qs = np.tile(q_values_input, (n_variants, 1)) + shift

    interpolated_curves = np.zeros((n_variants, len(q_values_prediction)))
    for i in range(n_variants):
        interpolated_curves[i] = np.interp(q_values_prediction, shifted_qs[i], corrected_reflectivity, )
    return interpolated_curves, shift


def curve_variant_log_mse(curve, variant_curves):
    """Calculate the log MSE of a curve and a :class:`ndarray` of curves"""
    errors = np.log10(curve) - np.log10(variant_curves)
    return np.mean(errors ** 2, axis=1)


def least_log_mean_squares_fit(data, predicted_labels, generator, output_preprocessor, fraction_bounds=(0.5, 0.5, 0.1)):
    """Fits the data with a model curve with ``scipy.optimize.minimize`` using ``predicted_labels`` as start values."""
    prep_labels = output_preprocessor.apply_preprocessing(predicted_labels)[0]
    start_values = np.array(prep_labels)[0]
    bounds = [(val - bound * abs(val), val + bound * abs(val)) for val, bound in zip(start_values, fraction_bounds)]
    fit_params = minimize(log_mse_loss, start_values, args=(data, generator, output_preprocessor), bounds=bounds)
    return output_preprocessor.restore_labels(np.atleast_2d(fit_params.x))


def log_mse_loss(prep_labels, data, generator, output_preprocessor):
    """MSE loss between a reflectivity curve and a model curve generated with the given normalized labels."""
    restored_labels = output_preprocessor.restore_labels(np.atleast_2d(prep_labels))
    model = generator.simulate_reflectivity(restored_labels,
                                            progress_bar=False)[0]
    loss = mean_squared_error(np.log10(data), np.log10(model))
    return loss


def mean_squared_error(array1, array2):
    """Returns element-wise mean squared error between two arrays."""
    if len(array1) != len(array2):
        raise ValueError(f'array1 and array2 must be of same length ({len(array1)} != {len(array2)})')
    else:
        error = np.asarray(array1) - np.asarray(array2)
        return np.mean(np.atleast_2d(error ** 2), axis=1)
