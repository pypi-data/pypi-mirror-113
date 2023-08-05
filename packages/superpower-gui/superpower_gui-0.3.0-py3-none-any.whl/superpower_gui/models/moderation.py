__all__ = ['ModerationModel']

import numpy as np
from traitlets import Bool, Float, List, Unicode

from ..mvc import Model


class ModerationModel(Model):
    # TODO Do values need to be store in traitlets in order to call R code?
    # TODO Does value assignment change type away from traitlet (see below)?
    """
        >>> x = Bool()
        >>> type(x)
        <class 'traitlets.traitlets.Bool'>
        >>> x = True
        >>> type(x)
        <class 'bool'>
    """

    standardized = Bool()
    nt = Float()
    b0 = Float()
    dependent_variable_name = Unicode()
    dependent_variable_standard_deviation = Float()

    predictor_names = List()
    predictor_is_continuous = List()
    predictor_level_names = List()
    predictor_proportions = List()
    predictor_standard_deviations = Float()
    predictor_slopes = List()
    predictor_interaction_slopes = List()

    power_covariate_names = List()
    power_covariate_is_continuous = List()
    power_covariate_level_names = List()
    power_covariate_propotions = List()
    power_covariate_standard_deviations = Float()
    power_covariate_slopes = List()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.land = None

    def setLanding(self):
        pass

    def setEstimates(self):
        pass

    def run(self):
        # TODO Caopy values from land into traitlets?
        return 1  # TODO Have model return usable value?