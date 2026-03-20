import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from scipy import stats


class RunTimeDataOperations:
    CONTROL_CHART_SUPERIOR_LIMIT = "95%"
    CONTROL_CHART_INFERIOR_LIMIT = "5%"

    def get_outliers(self, metrics: pd.DataFrame):
        outliers_indexes = []

        q1 = metrics.quantile(0.25)
        q3 = metrics.quantile(0.75)
        iqr = q3 - q1
        maximum = q3 + (1.5 * iqr)
        minimum = q1 - (1.5 * iqr)
        outlier_samples = metrics[(metrics < minimum) | (metrics > maximum)]
        outliers_indexes.extend(outlier_samples.index.tolist())

        outliers_indexes = list(set(outliers_indexes))
        return outliers_indexes

    def remove_outliers(
        self,
        release_1_metrics: pd.DataFrame,
        release_2_metrics: pd.DataFrame,
        release_1_endpoint_calls: pd.DataFrame,
        release_2_endpoint_calls: pd.DataFrame,
    ):
        outliers_indexes = list(
            set(
                [
                    *self.get_outliers(release_1_endpoint_calls.sum(axis=1)),
                    *self.get_outliers(release_2_endpoint_calls.sum(axis=1)),
                ]
            )
        )

        release_1_metrics.drop(outliers_indexes, inplace=True)
        release_1_metrics.reset_index(drop=True, inplace=True)

        release_2_metrics.drop(outliers_indexes, inplace=True)
        release_2_metrics.reset_index(drop=True, inplace=True)

        release_1_endpoint_calls.drop(outliers_indexes, inplace=True)
        release_1_endpoint_calls.reset_index(drop=True, inplace=True)

        release_2_endpoint_calls.drop(outliers_indexes, inplace=True)
        release_2_endpoint_calls.reset_index(drop=True, inplace=True)

    def get_random_forest(self, endpoint_calls, metrics):
        random_forest = RandomForestRegressor(random_state=0)
        return random_forest.fit(endpoint_calls, metrics)

    def is_normalized(self, release_dataframe: pd.DataFrame):
        _, p_value = stats.shapiro(release_dataframe)

        return p_value >= 0.05

    def calculate_violation_rate(
        self, release_1_metrics: pd.DataFrame, release_2_metrics: pd.DataFrame
    ):
        if (not self.is_normalized(release_1_metrics)) or (
            not self.is_normalized(release_2_metrics)
        ):
            return None

        release_1_metrics_statistic = release_1_metrics["metrics"].describe(
            percentiles=[0.05, 0.95]
        )

        superior_limit = release_1_metrics_statistic[self.CONTROL_CHART_SUPERIOR_LIMIT]
        inferior_limit = release_1_metrics_statistic[self.CONTROL_CHART_INFERIOR_LIMIT]

        sum_of_violation = 0

        for metric in release_2_metrics.values.tolist():
            if metric > superior_limit or metric < inferior_limit:
                sum_of_violation += 1

        return sum_of_violation / release_2_metrics.size

    def calculate_cliff_delta(
        self, release_1_metrics: pd.DataFrame, release_2_metrics: pd.DataFrame
    ):
        size = len(release_1_metrics)
        sum = 0

        for index_base in range(len(release_1_metrics)):
            for index_alvo in range(len(release_1_metrics)):
                value = 0

                if release_1_metrics[index_base] < release_2_metrics[index_alvo]:
                    value = -1

                elif release_1_metrics[index_base] > release_2_metrics[index_alvo]:
                    value = 1

                sum += value

        return abs(sum / (size * size))
