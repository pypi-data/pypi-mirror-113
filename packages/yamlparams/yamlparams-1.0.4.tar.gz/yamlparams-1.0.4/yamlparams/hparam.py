import yaml
from .dotdict import Dotdict


class Hparam(Dotdict):

    def __init__(self, file):
        super(Dotdict, self).__init__()
        hp_dict = self._load_hparam(file)
        hp_dotdict = Dotdict(hp_dict)
        for k, v in hp_dotdict.items():
            setattr(self, k, v)

    def _load_hparam(self, filename: str) -> dict:
        stream = open(filename, 'r')
        docs = yaml.load_all(stream, Loader=yaml.SafeLoader)
        hparam_dict = dict()
        for doc in docs:
            for k, v in doc.items():
                hparam_dict[k] = v
        return hparam_dict

    __getattr__ = Dotdict.__getitem__
    __setattr__ = Dotdict.__setitem__
    __delattr__ = Dotdict.__delitem__
