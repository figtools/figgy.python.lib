import json
from collections import OrderedDict
from .fig_store import FigStore
from .figs import ReplicatedFig, AppFig, SharedFig, MergeFig

TWIG = 'twig'
APP_FIGS = 'app_figs'
REPLICATE_FIGS = 'replicate_figs'
SHARED_FIGS = 'shared_figs'
MERGED_FIGS = 'merged_figs'


class ConfigWriter:
    """
    Writes the figgy.json file into the provided directory. If no directory is provided, writes the figgy.json
    to the local directory.
    """

    @staticmethod
    def write(fig_store: FigStore, file_name: str = "figgy.json", destination_dir=""):
        """
        Writes a figgy-compatible declarative configuration file to disk.

        @param: fig_store - A hydrated FigStore object used by your application to fetch configurations
        @param: file_name - Default: `figgy.json` (recommended). The name of the file that will be written.
        @param: destination_dir - Default: Current Directory..  The directory to write the `figgy.json` file to.
        """
        destination_dir = destination_dir.rstrip("/")

        figgy_config: OrderedDict = OrderedDict()
        figgy_config[TWIG] = fig_store.TWIG
        figgy_config[APP_FIGS] = []
        figgy_config[REPLICATE_FIGS] = {}
        figgy_config[SHARED_FIGS] = []
        figgy_config[MERGED_FIGS] = {}

        for fig in fig_store.figs:
            item = fig_store.__getattribute__(fig)
            if isinstance(item, AppFig):
                figgy_config[APP_FIGS].append(item.name)
            elif isinstance(item, ReplicatedFig):
                figgy_config[REPLICATE_FIGS][item.source] = item.name
            elif isinstance(item, SharedFig):
                figgy_config[SHARED_FIGS].append(item.name)
            elif isinstance(item, MergeFig):
                figgy_config[MERGED_FIGS][item.name] = item.pattern

        destination_dir = f'{destination_dir.rstrip("/")}/' if destination_dir else ''

        with open(f"{destination_dir}{file_name}", "w") as file:
            file.write(json.dumps(figgy_config, indent=4))
