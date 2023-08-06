import os


def get_os_env_flag(variable_name: str) -> bool:
    return os.environ.get(variable_name, "False").lower() == "true"
