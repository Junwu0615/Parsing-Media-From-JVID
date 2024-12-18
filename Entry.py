# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-15
"""
from Depend.ParsingMediaLogic import ParsingMediaLogic
from Depend.ArgumentParser import AP

class Entry:
    def __init__(self):
        self.type = None
        self.url = None
        self.path = None

    def main(self):
        ap = AP(self)
        ap.config_once()
        pm = ParsingMediaLogic(self)
        pm.main()

if __name__ == '__main__':
    entry = Entry()
    entry.main()