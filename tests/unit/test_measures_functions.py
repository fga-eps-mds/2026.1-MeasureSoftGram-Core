"""
Regression tests for default thresholds of aggregated normalized measures.

These tests pin the relationship between the canonical thresholds declared in
``DEFAULT_PRE_CONFIG`` and the defaults hardcoded in the measure functions in
``src/core/aggregated_normalized_measures.py``. Any divergence between them is a
bug — the function defaults should match the canonical configuration, otherwise
calling the function without a config silently produces a different
normalization than the production pipeline.
"""

import inspect

from core.aggregated_normalized_measures import run_time_measure
from staticfiles.default_pre_config import DEFAULT_PRE_CONFIG


def _find_measure_threshold(config, measure_key):
    """Walk DEFAULT_PRE_CONFIG looking for the named measure's max_threshold."""
    for characteristic in config["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:
            for measure in subcharacteristic["measures"]:
                if measure["key"] == measure_key:
                    return measure["max_threshold"]
    raise AssertionError(f"measure {measure_key!r} not found in DEFAULT_PRE_CONFIG")


def test_run_time_measure_default_max_threshold_matches_response_time_config():
    """
    Issue #14: run_time_measure has max_threshold default 0.33 hardcoded, but
    DEFAULT_PRE_CONFIG declares response_time with max_threshold 0.66. The
    function default must equal the canonical config value, otherwise
    direct calls (without a config) silently produce a different normalization
    than the production pipeline that always passes the config threshold.
    """
    canonical_max_threshold = _find_measure_threshold(
        DEFAULT_PRE_CONFIG, "response_time"
    )

    signature = inspect.signature(run_time_measure)
    function_default = signature.parameters["max_threshold"].default

    assert function_default == canonical_max_threshold, (
        f"run_time_measure default max_threshold={function_default} diverges "
        f"from DEFAULT_PRE_CONFIG response_time max_threshold="
        f"{canonical_max_threshold}"
    )
