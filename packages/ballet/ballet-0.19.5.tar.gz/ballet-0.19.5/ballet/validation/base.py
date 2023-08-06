from abc import ABCMeta, abstractmethod
from typing import Iterable, List, Optional, Union

import numpy as np
import pandas as pd

from ballet.feature import Feature


class BaseValidator(metaclass=ABCMeta):
    """Base class for a generic validator"""

    @abstractmethod
    def validate(self) -> bool:
        """Validate something and return whether validation succeeded"""
        pass


class FeaturePerformanceEvaluator(metaclass=ABCMeta):
    """Evaluate the performance of features from an ML point-of-view

    Implementing classes should be clear about their support for missing
    targets, i.e. NaN values in ``y_val``. For example, the subclass can raise
    an error indicating that it cannot be used for a problem, or it can choose
    to skip rows with missing values in the performance evaluation.

    Args:
        X_df: entities frame for fitting the features
        y_df: targets frame/series for fitting the features
        X_df_val: entities frame for evaluating the features
        y_val: target values for evaluating the features
        features: all collected features
        candidate_feature: the feature to evaluate
    """

    def __init__(self,
                 X_df: pd.DataFrame,
                 y_df: Union[pd.DataFrame, pd.Series],
                 X_df_val: pd.DataFrame,
                 y_val: np.ndarray,
                 features: Iterable[Feature],
                 candidate_feature: Feature):
        self.X_df = X_df
        self.y_df = y_df
        self.X_df_val = X_df_val
        self.y_val = y_val
        self.features = features
        self.candidate_feature = candidate_feature

    def __str__(self):
        return self.__class__.__name__


class FeatureAcceptanceMixin(metaclass=ABCMeta):

    @abstractmethod
    def judge(self) -> bool:
        """Judge whether feature should be accepted"""
        pass


class FeaturePruningMixin(metaclass=ABCMeta):

    @abstractmethod
    def prune(self) -> List[Feature]:
        """Prune existing features, returning list of features to remove"""
        pass


class FeatureAccepter(FeatureAcceptanceMixin, FeaturePerformanceEvaluator):
    """Accept/reject a feature to the project based on its performance"""
    pass


class FeaturePruner(FeaturePruningMixin, FeaturePerformanceEvaluator):
    """Prune features after acceptance based on their performance"""
    pass


class BaseCheck(metaclass=ABCMeta):

    def do_check(self, obj) -> bool:
        """Do the check and return whether an exception was *not* thrown"""
        try:
            self.check(obj)
        except Exception:
            return False
        else:
            return True

    @abstractmethod
    def check(self, obj) -> None:
        """Check something and throw an exception if the thing is bad"""
        pass

    def give_advice(self, feature) -> Optional[str]:
        """Description of how to resolve if the check fails"""
        return None
