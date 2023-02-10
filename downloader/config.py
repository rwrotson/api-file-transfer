import yaml

CONFIG_PATH = './config.yaml'

with open(CONFIG_PATH, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
