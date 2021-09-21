#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import orionsdk
import os,sys
import configparser
import requests
import argcomplete

import argparse

from EAT.procedure import config
from EAT.procedure.orion import Orion


global orion_un
global orion_pw

def eat():
    config.load_sw_base_conf()

     ####adding CLI Parsing
    parser = argparse.ArgumentParser(description='Navigate mac address tables to find a specified MAC.')
    subparsers = parser.add_subparsers(help="Choose between interactive or direct functionality", dest ='maincommand')

    orion_parser = subparsers.add_parser("orion", help="solarwinds commands").add_subparsers(dest="orion")
    add_group_orion_parser = orion_parser.add_parser("add_group", help="add groups")
    add_group_orion_parser.add_argument('groupfile', help='The file with groups in it')
    query_orion_parser = orion_parser.add_parser("query", help="query test")

    argcomplete.autocomplete(parser)
    cmdargs = parser.parse_args()

    orion = Orion(cmdargs, config)
    if cmdargs.maincommand == "orion":
        if cmdargs.orion == 'add_group':
            orion.add_group()
        if cmdargs.orion == 'query':
            orion.query()




if __name__ == "__main__":
    eat()