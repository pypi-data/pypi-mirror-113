from telegram.ext import MessageFilter
from ctparse import ctparse

class FilterUhrzeit(MessageFilter):
    def __init__(self):
        pass

    def filter(self, message):
        try:
            parse = ctparse('kurz nach mitternacht', timeout=1)
            return parse.resolution.isDateTime
        except:
            return False