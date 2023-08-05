# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_traits.ipynb (unless otherwise specified).

__all__ = ['IntArray', 'FloatArray', 'Int', 'Float', 'LinkAllMixin']

# Cell
from traittypes import Array
from traitlets import TraitType, HasTraits, Unicode
import traitlets
import numpy as np

# Cell
from .rpy import DTYPES, AS_DTYPE

# Cell
class IntArray(Array):
    def __init__(self, default_value=None, size=None, **kwargs):
        if size:
            assert 'default_value' not in kwargs, "Only one of 'size' or 'default_value' should be provided"
            kwargs['default_value'] = np.empty(size, dtype=DTYPES['int'])
        if default_value is not None:
            kwargs['default_value'] = default_value
        super().__init__(dtype=DTYPES['int'], **kwargs)

# Cell
class FloatArray(Array):
    def __init__(self, default_value=None, size=None, **kwargs):
        if size:
            assert 'default_value' not in kwargs, "Only one of 'size' or 'default_value' should be provided"
            kwargs['default_value'] = np.empty(size, dtype=DTYPES['float'])
        if default_value is not None:
            kwargs['default_value'] = default_value
        super().__init__(dtype=DTYPES['float'], **kwargs)

# Cell
class Int(TraitType):

    info_text = 'an integer compatible with R and numpy'

    def validate(self, obj, value):
        if isinstance(value, int) or (hasattr(value, 'dtype') and np.issubdtype(value.dtype, np.integer)):
            return AS_DTYPE['int'](value)
        self.error(obj, value)

# Cell
class Float(TraitType):

    info_text = 'an integer compatible with R and numpy'

    def validate(self, obj, value):
        if isinstance(value, int) or isinstance(value, float) or (hasattr(value, 'dtype') and np.issubdtype(value.dtype, np.floating)):
            return AS_DTYPE['float'](value)
        self.error(obj, value)

# Cell
class LinkAllMixin():

    def link_all(self, source, destination):
        dest_traits = destination.traits()
        for trait in source.traits():
            if trait in dest_traits:
                traitlets.link((source, trait), (destination, trait))