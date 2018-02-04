import ConfigParser
import logging

def message(mymessage, level="INFO"):
    logging.basicConfig(level=logging.DEBUG)
    if level == "INFO":
        logging.info(str(mymessage))
    elif level == "ERROR":
        logging.error(str(mymessage))
    else:
        logging.info(str(mymessage))

def masqueradeString(mystring):
    if mystring.startswith("+++"):
        return mystring
    else:
        masqueraded = mystring.encode('base64','strict').encode('base64','strict')
        mystring = "+++" + masqueraded
        return  mystring


def clearString(mystring):
    if mystring.startswith("+++"):
        myencodedstring = mystring[3:]
        mydecodedstring = myencodedstring.decode('base64','strict').decode('base64','strict')
        return mydecodedstring
    else:
        return mystring


def updateConfigFile(filename="" , section="" , key="" , value=""):
    myconfig = ConfigParser.ConfigParser()
    myconfig.read(filename)
    with open(filename, "w") as myfile:
        myconfig.set(section,key,value)
        myconfig.write(myfile)