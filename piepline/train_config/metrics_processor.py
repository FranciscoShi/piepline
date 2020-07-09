from piepline import events_container
from piepline.train_config.metrics import AbstractMetric, MetricsGroup
from piepline.train_config.stages import AbstractStage
from piepline.train import Trainer

__all__ = ['MetricsProcessor']


class MetricsProcessor:
    """
    Collection for all :class:`AbstractMetric`'s and :class:`MetricsGroup`'s
    """

    def __init__(self):
        self._metrics = []
        self._metrics_groups = []

    def subscribe_to_stage(self, stage: AbstractStage) -> 'MetricsProcessor':
        events_container.event(stage, 'EPOCH_END').add_callback(lambda s: self.reset_metrics())
        return self

    def subscribe_to_trainer(self, trainer: Trainer) -> 'MetricsProcessor':
        events_container.event(trainer, 'EPOCH_END').add_callback(lambda s: self.reset_metrics())
        return self

    def add_metric(self, metric: AbstractMetric) -> AbstractMetric:
        """
        Add :class:`AbstractMetric` object

        :param metric: metric to add
        :return: metric object
        :rtype: :class:`AbstractMetric`
        """
        self._metrics.append(metric)
        return metric

    def add_metrics_group(self, group: MetricsGroup) -> MetricsGroup:
        """
        Add :class:`MetricsGroup` object

        :param group: metrics group to add
        :return: metrics group object
        :rtype: :class:`MetricsGroup`
        """
        self._metrics_groups.append(group)
        return group

    def calc_metrics(self, output, target) -> None:
        """
        Recursive calculate all metrics

        :param output: predict value
        :param target: target value
        """
        for metric in self._metrics:
            metric.calc(output, target)
        for group in self._metrics_groups:
            group.calc(output, target)

    def reset_metrics(self) -> None:
        """
        Recursive reset all metrics values
        """
        for metric in self._metrics:
            metric.reset()
        for group in self._metrics_groups:
            group.reset()

    def get_metrics(self) -> {}:
        """
        Get metrics and groups as dict

        :return: dict of metrics and groups with keys [metrics, groups]
        """
        return {'metrics': self._metrics, 'groups': self._metrics_groups}