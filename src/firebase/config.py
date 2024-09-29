import yaml

firebase_credential_json = {}


# Load YAML file
def get_credentials():
    with open('src/firebase/firebase_config.yml', 'r') as yaml_file:
        firebase_credential_dict = yaml.safe_load(yaml_file)['Firebase_Env_Variables']

        # firebase_config = yaml.safe_load(yaml_file)
        # for firebase_config_dict in firebase_config['Firebase_Env_Variables']:
        #
        #     for key,value in firebase_config_dict.items():
        #         firebase_credential_json[key]=value

    return firebase_credential_dict
