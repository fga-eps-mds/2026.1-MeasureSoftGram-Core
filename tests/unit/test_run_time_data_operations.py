import pytest

from util.run_time_data_operations import RunTimeDataOperations


@pytest.fixture
def run_time_ops():
    return RunTimeDataOperations()


# Regression for issue #12: o loop interno de calculate_cliff_delta
# iterava sobre len(release_1_metrics) em vez de len(release_2_metrics),
# comparando release_1 x (slice de release_2 com tamanho de release_1).
# Quando |release_1| > |release_2| isso causa IndexError; quando
# |release_1| < |release_2| valores de release_2 sao silenciosamente
# descartados. Esses testes usam tamanhos distintos para expor o bug.


def test_cliff_delta_total_positive_separation_asymmetric_lengths(run_time_ops):
    # Todos elementos de release_1 sao maiores que todos de release_2.
    # Cliff's delta correto = +1.0 (a funcao retorna abs(), entao 1.0).
    release_1 = [10, 20, 30, 40, 50]
    release_2 = [1, 2, 3]
    assert run_time_ops.calculate_cliff_delta(release_1, release_2) == pytest.approx(1.0)


def test_cliff_delta_total_negative_separation_asymmetric_lengths(run_time_ops):
    # Todos elementos de release_1 sao menores que todos de release_2.
    # Cliff's delta correto = -1.0; com abs() vira 1.0.
    release_1 = [1, 2, 3]
    release_2 = [10, 20, 30, 40, 50]
    assert run_time_ops.calculate_cliff_delta(release_1, release_2) == pytest.approx(1.0)


def test_cliff_delta_asymmetric_known_value(run_time_ops):
    # release_1 = [1, 2, 3], release_2 = [2, 3, 4, 5].
    # Pares (x in r1, y in r2), n1*n2 = 12.
    # x>y: (3,2) -> 1 par.
    # x<y: (1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5) -> 9 pares.
    # x=y: (2,2),(3,3) -> 2 pares (contribuem 0).
    # delta = (1 - 9) / 12 = -0.6666...; abs = 0.6666...
    release_1 = [1, 2, 3]
    release_2 = [2, 3, 4, 5]
    assert run_time_ops.calculate_cliff_delta(release_1, release_2) == pytest.approx(
        8 / 12
    )
