from __future__ import annotations

from .executor import CompositeExecutor
from .utils import auth_settings_from_env_or_dev_insecure


def create_app():
    return CompositeExecutor().create_app(
        title="ARP Template Composite Executor",
        auth_settings=auth_settings_from_env_or_dev_insecure(),
    )


app = create_app()

