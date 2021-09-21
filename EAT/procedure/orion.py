#!/usr/bin/env python3

import re
import os
import sys
import requests
import urllib3
import orionsdk

class Orion:
    def __init__(self, cmdargs, config):
        # initialize values
        self.log_array = []
        self.cmdargs = cmdargs
        self.config = config
        self.log_path = os.path.abspath(os.path.join(os.sep, 'var', 'log', 'dnmt'))
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Supress the ssl unverified notification
    # self.config.logpath = os.path.join(os.path.expanduser(self.config.logpath), "logs", "UpgradeCheck",
    #                                   datetime.date.today().strftime('%Y%m%d'))

    def query(self):
        try:
            # npm_server = 'localhost'
            # username = 'admin'
            # password = ''
            #
            # verify = False
            # if not verify:
            #     from requests.packages.urllib3.exceptions import InsecureRequestWarning
            #     requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            swis = orionsdk.SwisClient(self.config.orion_sv, self.config.orion_un, self.config.orion_pw)

            print("Query Test:")
            results = swis.query("SELECT TOP 3 NodeID, DisplayName FROM Orion.Nodes")

            for row in results['results']:
                print("{NodeID:<5}: {DisplayName}".format(**row))
        except Exception as err:
            print(err)

    def add_group(self):
        try:
            swis = orionsdk.SwisClient(self.config.orion_sv, self.config.orion_un, self.config.orion_pw)

            #
            # CREATING A NEW GROUP
            #
            # Creating a new group with initial Cisco and Windows devices.
            #
            swis.invoke('Orion.Container', 'CreateContainer',
                        # group name
                        'Sample Python Group',

                        # owner, must be 'Core'
                        'Core',

                        # refresh frequency in seconds
                        60,

                        # Status rollup mode:
                        # 0 = Mixed status shows warning
                        # 1 = Show worst status
                        # 2 = Show best status
                        0,

                        # group description
                        'Group created by the Python sample script.',

                        # polling enabled/disabled = true/false
                        True,

                        # group members
                        [
                            {'Name': 'Cisco Devices', 'Definition': "filter:/Orion.Nodes[Vendor='Cisco']"},
                            {'Name': 'Windows Devices', 'Definition': "filter:/Orion.Nodes[Vendor='Windows']"}
                        ]
                        )

        except Exception as err:
            print("{}".format(err))

