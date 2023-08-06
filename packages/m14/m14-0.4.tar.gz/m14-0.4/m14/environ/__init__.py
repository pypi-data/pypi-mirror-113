#!/usr/bin/env python3
# coding: utf-8

__version__ = '0.4'

import volkanic
from volkanic.environ import GIMixinDirs


class GlobalInterface(volkanic.GlobalInterface, GIMixinDirs):
    package_name = 'm14.environ'

    def under_data_dir(self, *paths, mkdirs=False):
        path = '/data/local/{}'.format(self.project_name)
        path = self.conf.setdefault('data_dir', path)
        return super().under_data_dir(*paths, mkdirs=mkdirs)
