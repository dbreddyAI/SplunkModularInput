import ConfigParser

def masqueradeString(mystring):
    if mystring.startswith("+++"):
        return mystring
    else:
        masqueraded = mystring.encode('base64','strict')
        mystring = "+++" + masqueraded
        return  mystring


def clearString(mystring):
    if mystring.startswith("+++"):
        myencodedstring = mystring[3:]
        mydecodedstring = myencodedstring.decode('base64','strict')
        return mydecodedstring
    else:
        return mystring


def updateConfigFile(filename="" , section="" , key="" , value=""):
    myconfig = ConfigParser.ConfigParser()
    myconfig.read(filename)
    with open(filename, "w") as myfile:
        myconfig.set(section,key,value)
        myconfig.write(myfile)