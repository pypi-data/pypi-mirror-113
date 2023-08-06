import yamlenv
from .dotdict import Dotdict


class Hparam(Dotdict):

    def __init__(self, file):
        super(Dotdict, self).__init__()
        hp_dict = self._load_hparams(file)
        hp_dotdict = Dotdict(hp_dict)
        for k, v in hp_dotdict.items():
            setattr(self, k, v)

    def _load_hparams(self, filename: str) -> dict:
        stream = open(filename, 'r')
        hparam_dict = yamlenv.load(stream)
        return hparam_dict

    def __repr__(self):
        return f'Hparam {super().__repr__()}'

    __getattr__ = Dotdict.__getitem__
    __setattr__ = Dotdict.__setitem__
    __delattr__ = Dotdict.__delitem__
