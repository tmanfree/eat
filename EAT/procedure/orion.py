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
            swis = orionsdk.SwisClient(self.config.orion_sv, self.config.orion_un, self.config.orion_pw)

            results = swis.query("SELECT TOP 3 NodeID, DisplayName FROM Orion.Nodes")

            for row in results['results']:
                print("{NodeID:<5}: {DisplayName}".format(**row))
        except Exception as err:
            print(err)

    def add_group(self): #only assuming adding folders with parents
        file = open(self.cmdargs.groupfile, "r")
        for group_entry in file:
            # group formats:
            # structural folder,Parent_Folder,Child_Folder,Description
            # active folder,Parent_Folder,Child_Folder,Description,Building_Code,
            group_list = group_entry.rstrip().split(",")

            parent_name = group_list[1];
            child_name = group_list[2];
            description = group_list[3]
            if group_list[0] == "active folder":
                building_code = group_list[4]



            swis = orionsdk.SwisClient(self.config.orion_sv, self.config.orion_un, self.config.orion_pw)

            if len(group_list) == 1:
                pass #add a single group

            else: #add a group with parent

                try:
                    parent_check = swis.query("SELECT ContainerID FROM Orion.Container WHERE Name=@parent_name", parent_name=parent_name)  # set valid NodeID!
                    if len(parent_check['results']) == 1:#ID found
                        child_check = swis.query("SELECT ContainerID FROM Orion.Container WHERE Name=@parent_name",
                                             parent_name=child_name)  # set valid NodeID!
                        if (len(child_check['results'])) == 0: #ensure folder doesn't exist
                            if group_list[0] == "structural folder":
                                swis.invoke('Orion.Container', 'CreateContainerWithParent',
                                            parent_check['results'][0]['ContainerID'],  # parentID
                                            child_name,  # group name
                                            'Core',  # owner, must be 'Core'
                                            60,  # refresh frequency in seconds
                                            0,  # statuscalculator 0,1,2 mixed status, worst, best status
                                            description,  # group description
                                            True,
                                            []
                                            )

                            elif group_list[0] == "active folder":
                                member_list = []
                                if self.cmdargs.query is not None:
                                    query_list = self.cmdargs.query.split(",")
                                    for query_string in query_list:
                                        member_list.append({'Name':'{} Edge Node Query'.format(building_code),
                                                 'Definition': "filter:/Orion.Nodes[CustomProperties.Device_Type='{}' AND CustomProperties.Building='{}']".format(query_string,building_code)})

                                swis.invoke('Orion.Container', 'CreateContainerWithParent',
                                            parent_check['results'][0]['ContainerID'],#parentID
                                            child_name,# group name
                                            'Core',# owner, must be 'Core'
                                            60,# refresh frequency in seconds
                                            0,#statuscalculator 0,1,2 mixed status, worst, best status
                                            description,# group description
                                            True,# polling enabled/disabled = true/false
                                            # group members
                                            member_list
                                            )
                                print("Added Folder {} under {}".format(child_name,parent_name))
                        else:
                            print("Folder {} under {} exists already".format(child_name,parent_name))

                    else:
                        pass #create the parent container?
                        print("Parent folder {} not found, ignoring creating folder {}".format(group_list[1],group_list[2]))

                except Exception as err:
                    print("{}".format(err))

