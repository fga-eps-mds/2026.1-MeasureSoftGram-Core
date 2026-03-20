SUPPORTED_MEASURES = [
    {
        "passed_tests": {
            "metrics": [
                "tests",
                "test_failures",
                "test_errors",
            ],
        }
    },
    {
        "test_builds": {
            "metrics": [
                "test_execution_time",
                "tests",
            ],
        }
    },
    {
        "test_coverage": {
            "metrics": [
                "coverage",
            ],
        }
    },
    {
        "non_complex_file_density": {
            "metrics": [
                "functions",
                "complexity",
            ],
        }
    },
    {
        "commented_file_density": {
            "metrics": [
                "comment_lines_density",
            ],
        }
    },
    {
        "duplication_absense": {
            "metrics": [
                "duplicated_lines_density",
            ],
        }
    },
    {
        "team_throughput": {
            "metrics": [
                "total_issues",
                "resolved_issues",
            ],
        }
    },
    {
        "ci_feedback_time": {
            "metrics": [
                "sum_ci_feedback_times",
                "total_builds",
            ],
        }
    },
    {
        "response_time": {
            "metrics": [
                "endpoint_calls",
                "mean_response_time",
            ],
        }
    },
    {
        "cpu_utilization": {
            "metrics": [
                "endpoint_calls",
                "cpu_usage",
            ],
        }
    },
    {
        "memory_utilization": {
            "metrics": [
                "endpoint_calls",
                "memory_usage",
            ],
        }
    },
]
