import numpy as np
import pandas as pd

from util.exceptions import ImplicitMetricValueError, InvalidMetricValue


def resolve_metric_list_parameter(metric):
    """
    Resolves the metric list parameter to calculate a measure

    This functions converts the metric parameter to a pandas Series if it is a list (CalculateMeasures endpoint)
    otherwise it just returns the metric - already a pandas Series (Analysis endpoint).
    """
    return (
        pd.Series(metric, dtype=np.float64)
        if isinstance(metric, (list, np.ndarray))
        else metric
    )


def get_non_complex_files_density(
    data: dict,
):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality sub characteristic.
    """

    files_complexity = resolve_metric_list_parameter(data.get("complexity"))
    files_functions = resolve_metric_list_parameter(data.get("functions"))

    if len(files_complexity) != len(files_functions):
        raise ImplicitMetricValueError(
            (
                "Unable to get the implicit value of metric `number_of_file` "
                "because the size of the lists of values of metrics `complexity` "
                "and `functions` are not equal."
            )
        )
    else:
        number_of_files = data.get("number_of_files", len(files_complexity))

    has_none = files_complexity is None or files_functions is None
    has_zero = len(files_complexity) == 0 or len(files_functions) == 0

    if has_none or has_zero:
        return 0

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue(
            "The cyclomatic complexity of all files is lesser or equal than 0"
        )

    if files_functions.sum() <= 0:
        raise InvalidMetricValue(
            "The number of functions of all files is lesser or equal than 0"
        )

    complex_files_density = np.array(files_complexity / files_functions)

    return complex_files_density, number_of_files


def get_commented_files_density(data: dict):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality sub characteristic.
    """

    files_comment_lines_density = resolve_metric_list_parameter(
        data["comment_lines_density"]
    )

    number_of_files = data.get("number_of_files", len(files_comment_lines_density))

    has_none = files_comment_lines_density is None
    has_zero = len(files_comment_lines_density) == 0

    if has_none or has_zero:
        return 0, 0

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files comment lines density is lesser than 0"
        )

    return files_comment_lines_density, number_of_files


def get_absence_of_duplications(
    data: dict,
):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality sub characteristic.
    """

    files_duplicated_lines_density = resolve_metric_list_parameter(
        data["duplicated_lines_density"]
    )

    number_of_files = data.get("number_of_files", len(files_duplicated_lines_density))

    has_none = files_duplicated_lines_density is None
    has_zero = len(files_duplicated_lines_density) == 0

    if has_none or has_zero:
        return 0

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files duplicated lines density is lesser than 0"
        )

    return files_duplicated_lines_density, number_of_files


def get_passed_tests(data: dict[str, float]):
    """
    Calculates passed tests (em4)

    This function calculates the passed tests measure (em4)
    used to assess the testing status sub characteristic.
    """

    # number_of_tests está retornando valores incorretos
    number_of_tests = resolve_metric_list_parameter(data["tests"]).sum()
    number_of_test_errors = data["test_errors"]
    number_of_test_failures = data["test_failures"]

    number_of_fail_tests = number_of_test_errors + number_of_test_failures
    return number_of_tests, number_of_fail_tests


def get_fast_test_builds(data: dict[str, list]):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status sub characteristic.
    """

    execution_time = resolve_metric_list_parameter(data["test_execution_time"])
    number_of_tests = resolve_metric_list_parameter(data["tests"])
    number_of_files = len(execution_time)

    has_none = execution_time is None or number_of_tests is None
    has_zero = len(execution_time) == 0 or len(number_of_tests) == 0

    if has_none or has_zero:
        return 0, 0, 0

    return execution_time, number_of_files, number_of_tests


def get_test_coverage(data: dict):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status sub characteristic.
    """

    coverage = resolve_metric_list_parameter(data["coverage"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(coverage)

    has_none = coverage is None
    has_zero = len(coverage) == 0

    if has_none or has_zero:
        return 0

    return coverage, number_of_files


def get_team_throughput(data: dict[str, int]):
    """
    Calculates team throughput (em7)

    This function calculates the team throughput measure (em7)
    used to assess the testing status sub characteristic.
    """

    total_issues = data["total_issues"]
    resolved_issues = data["resolved_issues"]

    has_none = total_issues is None
    has_zero = total_issues == 0

    if has_none or has_zero:
        return 0

    return 100 * (resolved_issues / total_issues)


def get_ci_feedback_time(data: dict[str, int]):
    """
    Calculates CI Feedback Time (em8)

    This function calculates the CI Feedback Time measure (em8)
    used to assess the testing status sub characteristic.
    """

    total_builds = data["total_builds"]
    sum_ci_feedback_times = data["sum_ci_feedback_times"]

    has_none = total_builds is None
    has_zero = total_builds == 0

    if has_none or has_zero:
        return 0

    return sum_ci_feedback_times // total_builds
