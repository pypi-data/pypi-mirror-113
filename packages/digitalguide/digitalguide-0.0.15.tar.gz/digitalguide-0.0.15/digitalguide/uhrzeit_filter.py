from telegram.ext import MessageFilter
from ctparse import ctparse

class FilterUhrzeit(MessageFilter):
    def __init__(self, intent, confidence=0.8):
        self.intent = intent
        self.confidence = confidence

    def filter(self, message):
        try:
            parse = ctparse('kurz nach mitternacht', timeout=1)
            return parse.resolution.isDateTime
        except:
            return False