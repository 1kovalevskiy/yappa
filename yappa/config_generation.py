from pathlib import Path

from yappa.handle_wsgi import DEFAULT_CONFIG_FILENAME, load_yaml, save_yaml
from yappa.settings import DEFAULT_GW_CONFIG_FILENAME


def create_default_gw_config(filename=DEFAULT_GW_CONFIG_FILENAME):
    default_config = load_yaml(Path(Path(__file__).resolve().parent,
                                    DEFAULT_GW_CONFIG_FILENAME))
    save_yaml(default_config, filename)
    return default_config


def inject_function_id(gw_config, function_id, title="yappa gateway"):
    """
    accepts gw config as dict, finds where to put function_id, returns new dict
    """
    gw_config["info"].update(title=title)
    for path, methods in gw_config["paths"].items():
        for method, description in methods.items():
            yc_integration = description.get("x-yc-apigateway-integration")
            if yc_integration \
                    and yc_integration["type"] == "cloud_functions" \
                    and not yc_integration["function_id"]:
                yc_integration.update(function_id=function_id)
    return gw_config


HANDLERS = {
    "wsgi": "handle_wsgi.handle",
}


def get_yc_entrypoint(application_type):
    entrypoint = HANDLERS.get(application_type)
    if not entrypoint:
        raise ValueError(
            f"Sorry, supported app types are: {','.join(HANDLERS.keys())}."
        )
    return entrypoint


def create_default_config(filename=DEFAULT_CONFIG_FILENAME):
    default_config = load_yaml(Path(Path(__file__).resolve().parent,
                                    "yappa.yaml"))
    save_yaml(default_config, filename)
    return default_config