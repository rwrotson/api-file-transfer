import yaml

from downloader.consts import CONFIG_PATH

with open(CONFIG_PATH, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
