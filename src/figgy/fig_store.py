import logging
from dataclasses import dataclass
from typing import List

from .fig_svc import FigService

log = logging.getLogger(__name__)

ENV_LOCAL_RUN = 'LOCAL_RUN'


# All PS configurations are defined in our FigStore
@dataclass
class FigStore:
    TWIG: str

    @property
    def figs(self) -> List[str]:
        return [a for a in dir(self) if not a.startswith('__') and not a == 'TWIG' and not a == 'figs']

    def __init__(self, fig_svc: FigService, lazy_load: bool = False):
        # A little magic, setting the twig attribute for each FIG for a better user experience
        for fig in self.figs:
            self.__getattribute__(fig).twig = self.TWIG

        if lazy_load:
            for fig in self.figs:
                self.__getattribute__(fig).fig_svc = fig_svc
        else:
            for fig in self.figs:
                self.__getattribute__(fig).value = fig_svc.get_fig(self.__getattribute__(fig).name, prefix=self.TWIG)
