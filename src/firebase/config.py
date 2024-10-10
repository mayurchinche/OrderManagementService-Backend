import yaml

firebase_credential_json = {}


# Load YAML file
def get_credentials():
    with open("src/firebase/firebase_config.yml", "r") as yaml_file:
        firebase_credential_dict = yaml.safe_load(yaml_file)["Firebase_Env_Variables"]
    return firebase_credential_dict
