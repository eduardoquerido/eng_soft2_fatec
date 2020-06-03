from enum import Enum, EnumMeta
from collections import namedtuple

EnumOpt = namedtuple('EnumOpt', ['opt', 'label'])


class TupleEnumMeta(EnumMeta):
    @property
    def choices(self):
        return [(e.opt, e.label) for e in self]


class TupleEnum(Enum, metaclass=TupleEnumMeta):
    @property
    def label(self):
        return self.value.label

    @property
    def opt(self):
        return self.value.opt
