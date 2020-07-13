import argparse
import yaml
import os

class _Config:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as y:
            self.config = yaml.safe_load(y)

    def __getattr__(self, name):
        return self.config[name]

config=_Config()