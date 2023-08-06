#!/usr/bin/python3

# Copyright (C) 2018 Miguel Simoes, miguelrsimoes[a]yahoo[.]com
# For conditions of distribution and use, see copyright notice in lnsync.py


# pylint: disable=unused-import

from lnsync_pkg.modaltype import onofftype, ONLINE, OFFLINE

class PropDBException(Exception):
    pass

class PropDBError(PropDBException):
    pass

class PropDBNoValue(PropDBException):
    pass

class PropDBStaleValue(PropDBException):
    pass

class PropDBManager(metaclass=onofftype):
    @staticmethod
    def get_glob_patterns():
        return []

    def __init__(self, *args, **kwargs):
        pass
