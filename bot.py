from os import path

import none

import config

if __name__ == '__main__':
    none.init(config)
    none.load_plugins(path.join(path.dirname(__file__), 'ffxiv', 'plugins'),
                      'ffxiv.plugins')
    none.run()
