import pytest

from core.aggregated_normalized_measures import ci_feedback_time
from tests.utils.aggregated_normalized_measures_data import (
    INVALID_METRICS_TEST_DATA,
    INVALID_THRESHOLD_TEST_DATA,
    SUCCESS_TEST_DATA,
)
from util.exceptions import InvalidMetricValue, InvalidThresholdValue


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,error_msg",
    INVALID_METRICS_TEST_DATA,
)
def test_aggregated_normalized_measures_invalid_metrics(
    aggregated_normalized_measure, data_frame, error_msg
):
    """
    Test cases in which the interpretation functions should raise an InvalidMetricValue exception
    """

    with pytest.raises(InvalidMetricValue) as error:
        aggregated_normalized_measure(data_frame)

    assert str(error.value) == error_msg


@pytest.mark.parametrize(
    "aggregated_normalized_measure,data_frame,expected_result",
    SUCCESS_TEST_DATA,
)
def test_aggregated_normalized_measures_success(
    aggregated_normalized_measure, data_frame, expected_result
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """

    result = aggregated_normalized_measure(data_frame)

    function_call = f"{aggregated_normalized_measure.__name__}({data_frame})"

    assert pytest.approx(result) == expected_result

    assert 0 <= result <= 1.0, f"Expected: 0 <= {function_call} <= 1.0"


@pytest.mark.parametrize(
    "aggregated_normalized_measure,params,error_msg",
    INVALID_THRESHOLD_TEST_DATA,
)
def test_aggregated_normalized_measures_invalid_thresholds(
    aggregated_normalized_measure, params, error_msg
):
    """
    Test cases in which the interpretation functions should return a valid measure
    """
    with pytest.raises(InvalidThresholdValue) as error:
        aggregated_normalized_measure(**params)

    assert str(error.value) == error_msg


def test_ci_feedback_time_fast_pipeline_yields_high_measure():
    """
    Regression test for issue #15.

    Semantica: ci_feedback_time mede o tempo medio de feedback do CI;
    menos tempo = melhor (mesma convencao de fast_test_builds, que usa
    gain_interpretation=-1). Portanto um pipeline rapido (60s/build,
    bem dentro do limite max_threshold=900) deve produzir uma medida
    ALTA (proximo de 1.0), nao baixa.

    Hoje (bug) o codigo usa gain_interpretation=+1, invertendo a
    interpretacao e retornando ~0.066 para esse cenario. Esperamos
    >= 0.5 (idealmente ~0.934).
    """
    data_frame = {
        "total_builds": 10,
        "sum_ci_feedback_times": 600,  # media de 60s/build (rapido)
    }

    result = ci_feedback_time(data_frame)

    assert result >= 0.5, (
        f"CI rapido (60s/build) deveria render medida alta, mas obteve {result}. "
        "Provavel inversao de gain_interpretation em ci_feedback_time."
    )


def test_ci_feedback_time_no_builds_yields_neutral_measure():
    """
    Regression test for issue #24.

    Semantica: quando total_builds == 0 nao existe dado de feedback do
    CI no periodo (time sem pipeline rodando). Nesse caso a medida nao
    pode valer 1.0, pois isso premiaria a ausencia de CI como se fosse
    o pipeline mais rapido possivel. Tambem nao deve valer 0.0 (punicao
    maxima). O comportamento correto e retornar um score neutro (0.5).

    Hoje (bug) get_ci_feedback_time retorna 0 para total_builds == 0, e
    esse 0 satura a interpolacao em 0, resultando em 1 - 0 = 1.0.
    """
    data_frame = {
        "total_builds": 0,
        "sum_ci_feedback_times": 0,
    }

    result = ci_feedback_time(data_frame)

    assert result == 0.5, (
        f"Sem builds no periodo a medida deveria ser neutra (0.5), "
        f"mas obteve {result}. Ausencia de CI nao pode render nota maxima."
    )
