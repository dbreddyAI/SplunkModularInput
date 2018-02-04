import sys
import logging
import os

from splunklib.modularinput import *

import ConfigParser
from SharedAPIs.SharedAPIs import *


def do_work(input_name, ew, symbol):
    EventWriter.log(ew, EventWriter.INFO, "JORDI %s" % symbol)
    data = symbol
    splunk_home = os.getenv("SPLUNK_HOME")
    myscript = sys.argv[0]
    basedir = os.path.dirname(os.path.dirname(sys.argv[0]))
    inputsfile = basedir + "/local/inputs.conf"
    mydata = "JORDI LOGS: PARAMETER:{} SPLUNK_HOME:{} MYSCRIPT:{} basedir:{} inputsfile:{}".format(data,splunk_home, myscript, basedir, inputsfile)
    message(mydata)
    EventWriter.log(ew, EventWriter.INFO, mydata)
    event.data = mydata
    ew.write_event(event)


class MyScript(Script):

    def get_scheme(self):
        scheme = Scheme("My test input")
        scheme.description = "My test input prototype"
        scheme.use_external_validation = True
        scheme.use_single_instance = False

        username_argument = Argument("username")
        username_argument.data_type = Argument.data_type_string
        username_argument.description = "username"
        username_argument.required_on_create = True
        scheme.add_argument(username_argument)


        password_argument = Argument("password")
        password_argument.data_type = Argument.data_type_string
        password_argument.description = "password"
        password_argument.required_on_create = True
        scheme.add_argument(password_argument)

        return scheme

    def validate_input(self, validation_definition):
        message("lala: im in")


    def stream_events(self, inputs, ew):
        self.masqueradeConfig()
        message("JORDI executed")
        for input_name, input_item in inputs.inputs.iteritems():
            symbol = str(input_item["username"])
            do_work(input_name, ew, symbol)


    def masqueradeConfig(self):
        message("masquerade config")
        self.SPLUNK_HOME = os.getenv("SPLUNK_HOME")
        self.BASEDIR = os.path.dirname(os.path.dirname(sys.argv[0]))
        self.INPUTSFILE = self.BASEDIR + "/local/inputs.conf"
        myconfig = ConfigParser.ConfigParser()
        myconfig.read(self.INPUTSFILE)
        for mysection in myconfig.sections():
            for (mykey, myvalue) in myconfig.items(mysection):
                message("section:{} key:{} value:{}".format(mysection, mykey, myvalue))
                if (mykey == "username" or mykey == "password") and not myvalue.startswith("+++"):
                    mynewvalue = masqueradeString(myvalue)
                    message("To masquerade key={0} value={1} into key={0} value={2}".format(mykey, myvalue, mynewvalue))
                    updateConfigFile(self.INPUTSFILE, mysection, mykey, mynewvalue)


def mytest():
    splunk_home = os.getenv("SPLUNK_HOME")
    myscript = sys.argv[0]
    basedir = os.path.dirname(os.path.dirname(sys.argv[0]))
    inputsfile = basedir + "/local/inputs.conf"
    mydata = "JORDI LOGS: SPLUNK_HOME:{} MYSCRIPT:{} basedir:{} inputsfile:{}".format(splunk_home,
                                                                                                   myscript, basedir,
                                                                                                   inputsfile)
    message(str(mydata))
    myconfig = ConfigParser.ConfigParser()
    myconfig.read(inputsfile)
    for mysection in myconfig.sections():
        for (mykey, myvalue) in myconfig.items(mysection):
            message("section:{} key:{} value:{}".format(mysection,mykey,myvalue))
            if ( mykey == "username" or mykey == "password" ) and not myvalue.startswith("+++"):
                mynewvalue = masqueradeString(myvalue)
                message("To masquerade key={0} value={1} into key={0} value={2}".format(mykey, myvalue, mynewvalue))
                updateConfigFile(inputsfile, mysection, mykey, mynewvalue)
    pass

if __name__ == "__main__":
    #mytest()
    MyScript().run(sys.argv)