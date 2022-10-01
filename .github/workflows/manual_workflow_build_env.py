import yaml
import os
import json


def merge(source: dict, destination: dict):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, dict())
            merge(value, node)
        else:
            destination[key] = value
    return destination


def create_env_file(config: dict):
    with open("foundation.env", "w") as file:
        create_env(config, file)


def create_env(
    config: dict,
    env_file,
    grandparent_key: str = None,
    parent_key: str = None,
):
    for key, value in config.items():
        if isinstance(value, dict):
            create_env(config[key], env_file, parent_key, key)
        else:
            output_string = f"{key}={value}"
            if isinstance(value, list):
                quoted_json = json.dumps(value).replace('"', '\\"')
                output_string = f"{key}='{quoted_json}'"

            if parent_key:
                output_string = f"{parent_key}_{output_string}"

            if grandparent_key:
                output_string = f"{grandparent_key}_{output_string}"

            env_file.write(f"foundation_{output_string}\n")
            out_string = f'echo "foundation_{output_string}" >> $GITHUB_ENV'
            os.system(out_string)


foundation_config_file = os.environ.get("FOUNDATION_CONFIG_FILE")

with open(foundation_config_file, "r") as file:
    foundation_config = dict(yaml.load(file, Loader=yaml.FullLoader))

foundation_branches_config: dict = foundation_config.get("branches", dict())
if foundation_branches_config:
    foundation_config.pop("branches")

github_ref = os.environ.get("GITHUB_REF_NAME")
if "OVERRIDE_REF_NAME" in os.environ:
    github_ref = os.environ.get("OVERRIDE_REF_NAME")
if github_ref and (github_ref in foundation_branches_config):
    branch_config = foundation_branches_config.get(github_ref, dict())
    foundation_config = merge(branch_config, foundation_config)

create_env_file(foundation_config)
