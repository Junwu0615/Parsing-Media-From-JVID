# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-15
"""
from argparse import ArgumentParser, Namespace

class AP:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def parse_args() -> Namespace:
        parse = ArgumentParser()
        parse.add_argument('-t', '--type',
                           help='give a want todo type | ex: image / mp4',
                           default='image', type=str)

        parse.add_argument('-u', '--url',
                           help="give a url of JVID | ex: 'https://www.jvid.com/v/[PAGE_ID]'",
                           default='', type=str)

        parse.add_argument('-p', '--path',
                           help="give a save path | ex: './Media/'",
                           default='Media', type=str)

        return parse.parse_args()

    def config_once(self):
        args = AP.parse_args()
        self.obj.type = args.type
        self.obj.url = args.url
        self.obj.path = args.path