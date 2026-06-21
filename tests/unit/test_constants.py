from resources.constants import AVAILABLE_PRE_CONFIGS


def test_memory_utilization_uses_memory_usage_metric():
    """Issue #13: memory_utilization listava cpu_usage por copy-paste de
    cpu_utilization. A medida deve consumir memory_usage (métrica canônica
    em supported_metrics.py), nunca cpu_usage."""
    memory_utilization = AVAILABLE_PRE_CONFIGS["measures"]["memory_utilization"]
    metrics = memory_utilization["metrics"]

    assert "cpu_usage" not in metrics, (
        "memory_utilization não pode listar cpu_usage como métrica "
        "(copy-paste bug do cpu_utilization — issue #13)."
    )
    assert "memory_usage" in metrics, (
        "memory_utilization deve listar memory_usage como métrica, "
        "alinhado com supported_metrics.py."
    )
