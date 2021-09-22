# Edge Api Tool (eat)
The Edge Api Tool *(EAT)* is intended to house various functions that
interact with APIs of various tools. **All functions have the -h flag that will
*not* run the program, but will return with a help text that should provide more information on how to run it.**

A config file (config.text) is required to get user information (username/pass/snmp/etc)

Current functionality:

### Orion commands
* **add_group** - eat.py orion add_group *groupfile* -q *"custom_query_1,custom_query_2"*.  
Fairly hard coded into specific custom_fields in solar winds
 
 
 ## Requirements

* Python 3.5
* Python packages listed in setup.py
* a config.text file where you will run the command with the following information in it:
    * [SWITCHCRED]
    * username=*USERNAME*
    * password=*PASSWORD*
    * enable=*ENABLEPASS*
    * [SNMP]
    * ro=*SNMPV2ROSTRING*
    * rw=*SNMPV2RWSTRING*
    * [PATH]
    * logpath=*~*