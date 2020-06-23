import logging
import os
from abc import ABC
from typing import Optional, List, Union

# JSON Key Constants
from .fig_svc import FigService

FIG_MISSING = "FIG NOT SET"
log = logging.getLogger(__name__)


class ConfigurationMissingException(Exception):
    def __init__(self, fig_name):
        super().__init__(f"The configuration: {fig_name} "
                         f"was not found in Parameter Store or as an environment variable override.")


class Fig(ABC):
    twig: str = None

    """
    Represents a single fig in ParameterStore.
    """

    def __init__(self, name: str, twig: Optional[str] = None):
        self._name = name
        self.twig = twig

    @property
    def env_name(self):
        """
        Return the ENV Variable name that can override any remote configurations.
        """
        return self.base_name.replace("/", "_").replace("-", "_").upper().rstrip("_").lstrip("_")


    @property
    def base_name(self):
        """
        Return the base/path/to/the/fig without the TWIG
        """
        return self._name

    @property
    def name(self):
        """
        Return the /full/path/to/the/fig in ParameterStore
        """
        if self.twig:
            if not self._name.startswith(self.twig):
                return f'{self.twig.rstrip("/")}/{self._name.lstrip("/")}'
            else:
                return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def fig_svc(self):
        return self._fig_svc

    @fig_svc.setter
    def fig_svc(self, fig_svc: FigService):
        self._fig_svc = fig_svc

    @property
    def value(self) -> str:
        if os.environ.get(self.env_name):
            self._value = os.environ.get(self.env_name)
            log.debug(f'{self.env_name} found in environment. Using value: {self._value}')
        else:
            if not hasattr(self, '_value') or not self._value:
                if hasattr(self, '_fig_svc') and self._fig_svc:
                    log.info(f"Looking up fig: {self.name}")
                    self._value = self._fig_svc.get_fig(self.name)

        # Either we can't find the value, or there is a bug in this software
        if not self._value:
            raise ConfigurationMissingException(self.name)

        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return self.value

    def __eq__(self, o):
        return self.name == o.name

class AppFig(Fig):
    """
    Represents a single configuration that is specific to your application.
    """
    default: Optional[str] = None

    def __init__(self, name: str, default: Optional[str] = None):
        super().__init__(name=name)
        self.default = default


class ReplicatedFig(Fig):
    """
    Defines a parameter that is a global, shared, configuration that you want our application to have
    access to in its FigStore.
    """
    source: str

    def __init__(self, name: str, source: str):
        super().__init__(name=name)
        self.source = source


class SharedFig(Fig):
    """
    Defines a parameter owned by an outside party that must be shared with your application for it to run.

    E.G - DB Credentials, API Keys, etc.
    """
    def __init__(self, name: str):
        super().__init__(name=name)


class MergeFig(Fig):
    """
    Creates a single parameter by combining a group of parameters into an "uber-parameter". This is ideal for
    building out DB Connection URLs, etc.
    """
    pattern: List[Union[str, Fig]]

    def __init__(self, name: str, pattern: List[Union[str, Fig]], uri_encode: List[Fig] = None):
        super().__init__(name=name)
        self.pattern = pattern
        self.uri_encode = uri_encode if uri_encode else []

    @property
    def pattern(self):
        translated_pattern = []
        for p in self._pattern:
            if hasattr(p, 'name'):
                suffix = ''
                if p in self.uri_encode:
                    suffix = ':uri'

                translated_pattern.append(f'${{{p.name}{suffix}}}')
            else:
                translated_pattern.append(p)

        return translated_pattern

    @pattern.setter
    def pattern(self, pattern: List[Union[str, Fig]]):
        self._pattern = pattern
