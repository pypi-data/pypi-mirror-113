"""Implement a loader for plaster using yaml format."""
import pathlib
import logging
import logging.config
from typing import Callable

import pkg_resources
import plaster
from dynaconf import Dynaconf


class MissingConfigSectionException(Exception):
    """
    This exception is raised if a consumer of the Loader requires a section
    that does not exist in the proviced dynaconf configuration"""


def resolve_use(use: str, entrypoint: str) -> Callable:
    try:
        pkg, name = use.split("#")
    except ValueError:
        pkg, name = use, "main"
    try:
        scheme, pkg = pkg.split(":")
    except ValueError:
        scheme = "egg"
    if scheme != "egg":
        raise ValueError(f"{use}: unsupported scheme {scheme}")

    distribution = pkg_resources.get_distribution(pkg)
    runner = distribution.get_entry_info(entrypoint, name)
    return runner.load()


class Loader(plaster.ILoader):
    def __init__(self, uri):
        self.uri = uri

        path = pathlib.Path(self.uri.path)
        self.defaults = {
            "__file__": str(path.absolute()),
            "here": str(path.parent),
        }
        self._conf = Dynaconf(
            settings_files=path, load_dotenv=True, environments=True
        )
        # guarantee that pserve section exists in config
        self._conf['pserve'] = self._conf.get('pserve', {})

    def get_sections(self):
        return tuple(self._conf.keys())

    def get_settings(self, section=None, defaults=None):
        # fallback to the fragment from config_uri if no section is given
        if not section:
            section = self.uri.fragment or "app"
        # if section is still none we could fallback to some
        # loader-specific default

        result = self.defaults.copy()
        if defaults is not None:
            result.update(defaults)

        try:
            settings = self._conf[section].copy()
        except KeyError:
            raise MissingConfigSectionException(
                " ".join((
                    f"\nMissing section {section}!",
                    "\nYour consumer of the plaster_dynaconf Loader requires",
                    "this section to be in the configuration.",
                ))
            )

        for key, val in settings.items():
            if isinstance(val, str):
                if "%(here)s" in val:
                    settings[key] = val % self.defaults
        return settings

    def get_wsgi_app_settings(self, name=None, defaults=None):
        return self.get_settings(name, defaults)

    def setup_logging(self, config_vars):
        try:
            logging.config.dictConfig(
                self._conf["logging"]
            )
        except KeyError:
            raise MissingConfigSectionException(
                " ".join((
                    "\nMissing section logging!",
                    "\nYour consumer of the plaster_dynaconf Loader requires",
                    "setup_logging which requires the logging to be set in",
                    "the logging section of the dynaconf config.",
                    "\nThe logging config has to be in the dictConfig format",
                    "of the standard logging module. See ",
                    "https://docs.python.org/3/library/logging.config.html?highlight=logging%20dictconfig#configuration-dictionary-schema",  # noqa: E501
                    "for details.",
                ))
            )

    def get_wsgi_server(self, name=None, defaults=None):
        settings = self.get_settings("server", defaults)
        server = resolve_use(settings.pop("use"), "paste.server_runner")
        return lambda app: server(app, self.defaults, **settings)

    def get_wsgi_app(self, name=None, defaults=None):
        settings = self.get_settings(name, defaults)
        use = resolve_use(settings.pop("use"), "paste.app_factory")
        return use(defaults, **settings)
