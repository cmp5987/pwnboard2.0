from os import walk
from typing import List


class PluginManager():
    def __init__(self):
        callback_hooks: List[function]
        callback_hooks = []

    def search_plugins(self):
        filenames = next(walk('./api/plugins'), (None, None, [])
                         )[2]
        print(filenames)


if __name__ == '__main__':
    pluginManager = PluginManager()
    pluginManager.search_plugins()
