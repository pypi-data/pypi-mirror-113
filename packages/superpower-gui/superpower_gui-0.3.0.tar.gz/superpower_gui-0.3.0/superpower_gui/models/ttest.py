# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/models.ttest.ipynb (unless otherwise specified).

__all__ = ['TTestModel', 'SingleSampleModel', 'DiffPairedSamplesModel', 'PairedSamplesModel', 'IndependentSamplesModel']

# Cell
from traitlets import Float, Int, observe, Bool, Unicode
import math

# Cell
from ..mvc import Model
from .error_bars import ErrorBarsModel
from ..superpower.ttest import TTest

# Cell
class TTestModel(Model):

    m = Float()
    sd = Float()
    d = Float()
    N = Int()

    def __init__(self):
        super().__init__()
        self.function = TTest()

    def setLanding(self):
        self.errBars = ErrorBarsModel(nBars=1, nGroups=1)
        self.errBars.setEstimates()
        self.errBars.labels=['']

    def setEstimates(self):
        with self.hold_trait_notifications():
            self.m = 0.2
            self.sd = 1
            self.N = 200


    @observe('m')
    def observe_mean(self, change):
        self.d = change['new'] / self.sd
        self.errBars.setHeight(0, change['new'])
        return change['new']

    @observe('sd')
    def observe_sd(self, change):
        self.d = self.m / change['new']
        self.errBars.setError(0, change['new'])
        return change['new']

# Cell
class SingleSampleModel(TTestModel):

    def run(self):
        kwargs = self.getTraits()
        kwargs['type'] = 'singleSample'
        kwargs['means1'] = kwargs.pop('m')
        kwargs['sd1'] = kwargs.pop('sd')
        return self.function.run(**kwargs)

class DiffPairedSamplesModel(TTestModel):

    def run(self):
        #res = function.run(meanDifference = .2, sd1=1, N=200, type='pairedSamples')
        kwargs = self.getTraits()
        kwargs['type'] = 'pairedSamples'
        kwargs['sd1'] = kwargs.pop('sd')
        kwargs['meanDifference'] = kwargs.pop('m')
        return self.function.run(**kwargs)

# Cell
class PairedSamplesModel(Model):

    label1 = Unicode()
    label2 = Unicode()

    m1 = Float()
    m2 = Float()
    sd1 = Float()
    sd2 = Float()
    d = Float()
    N = Int()
    r = Float()

    def __init__(self):
        super().__init__()
        self.function = TTest()

    def run(self):
        kwargs = self.getTraits()
        kwargs['corr'] = kwargs.pop('r')
        kwargs['type'] = 'pairedSamples'
        kwargs['means1'] = kwargs.pop('m1')
        kwargs['means2'] = kwargs.pop('m2')
        return self.function.run(**kwargs)

    def setLanding(self):
        self.errBars = ErrorBarsModel(nBars=2,nGroups=1)
        self.errBars.setEstimates()
        self.label1 = 'A'
        self.label2 = 'B'

    def setEstimates(self):
        self.errBars.setEstimates()
        with self.hold_trait_notifications():
            self.m1 = 1
            self.m2 = 1.2
            self.sd1 = 1
            self.sd2 = 1
            self.N = 200
            self.r = .8

    @observe('label1')
    def observe_label1(self, change):
        self.errBars.labels[0] = change['new']
        return change['new']

    @observe('label2')
    def observe_label2(self, change):
        self.errBars.labels[1] = change['new']
        return change['new']

    @observe('m1')
    def observe_m1(self, change):
        self.errBars.setHeight(0, change['new'])
        self.calc_d(change['new'], self.m2, self.r, self.sd1, self.sd2)
        return change['new']

    @observe('m2')
    def observe_m2(self, change):
        self.errBars.setHeight(1, change['new'])
        self.calc_d(self.m1, change['new'], self.r, self.sd1, self.sd2)
        return change['new']

    @observe('r')
    def observe_ratio(self, change):
        assert change['new'] < 1, 'Ratio must be less than 1.'
        self.calc_d(self.m1, self.m2, change['new'], self.sd1, self.sd2)
        return change['new']

    @observe('sd1')
    def observe_sd1(self, change):
        self.errBars.setError(0, change['new'])
        self.calc_d(self.m1, self.m2, self.r, change['new'], self.sd2)
        return change['new']

    @observe('sd2')
    def observe_sd2(self, change):
        self.errBars.setError(1, change['new'])
        self.calc_d(self.m1, self.m2, self.r, self.sd1, change['new'])
        return change['new']

    def calc_d(self, m1, m2, r, sd1, sd2):
        self.d = round((m1 - m2) / math.sqrt(sd1**2 + sd2**2 - 2 * sd1 * sd2 * r), 2)

# Cell
class IndependentSamplesModel(Model):

    label1 = Unicode()
    label2 = Unicode()

    m1 = Float()
    m2 = Float()
    sd1 = Float()
    sd2 = Float()
    d = Float()
    N = Int()
    ratio = Float()
    n1 = Int()
    n2 = Int()

    def __init__(self):
        super().__init__()
        self.function = TTest()

    def run(self):
        kwargs = self.getTraits()
        kwargs['type'] = 'indSamples'
        kwargs['means1'] = kwargs.pop('m1')
        kwargs['means2'] = kwargs.pop('m2')
        kwargs.pop('n1')
        kwargs.pop('n2')
        return self.function.run(**kwargs)

    def setLanding(self):
        self.errBars = ErrorBarsModel(nBars=2,nGroups=1)
        self.errBars.setEstimates()
        self.label1 = 'A'
        self.label2 = 'B'


    def setEstimates(self):
        with self.hold_trait_notifications():
            self.m1 = 1
            self.m2 = 1.2
            self.sd1 = 1
            self.sd2 = 1
            self.ratio = 1
            self.N = 200
            self.n1


    @observe('label1')
    def observe_label1(self, change):
        self.errBars.labels[0] = change['new']
        return change['new']

    @observe('label2')
    def observe_label2(self, change):
        self.errBars.labels[1] = change['new']
        return change['new']

    @observe('m1')
    def observe_m1(self, change):
        self.errBars.setHeight(0, change['new'])
        self.calc_d(change['new'], self.m2, self.ratio, self.sd1, self.sd2)
        return change['new']

    @observe('m2')
    def observe_m2(self, change):
        self.errBars.setHeight(1, change['new'])
        self.calc_d(self.m1, change['new'], self.ratio, self.sd1, self.sd2)
        return change['new']

    @observe('ratio')
    def observe_ratio(self, change):
        self.calc_d(self.m1, self.m2, change['new'], self.sd1, self.sd2)
        n2 = self.N / (change['new'] + 1)
        self.n1 = int(n2 * change['new'])
        self.n2 = int(n2)
        return change['new']

    @observe('sd1')
    def observe_sd1(self, change):
        self.errBars.setError(0, change['new'])
        self.calc_d(self.m1, self.m2, self.ratio, change['new'], self.sd2)
        return change['new']

    @observe('sd2')
    def observe_sd2(self, change):
        self.errBars.setError(1, change['new'])
        self.calc_d(self.m1, self.m2, self.ratio, self.sd1, change['new'])
        return change['new']

    def calc_d(self, m1, m2, ratio, sd1, sd2):
        self.d = round((m1 - m2) / math.sqrt((ratio * sd1**2 + sd2**2) / (ratio + 1)), 2)