import yamlenv
from .hparam import Hparam
# Backward compatibility


def load(document: str):
    return yamlenv.load(open(document))


def dump(config: Hparam):
    yamlenv.dump(config)
