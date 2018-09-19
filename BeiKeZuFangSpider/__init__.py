# -*- coding: utf-8 -*- #
"""
Created on 2018年9月19日
@author: Leo
"""

import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))
