#!/usr/bin/env python

class NeedUserInteraction(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class UnknownError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
