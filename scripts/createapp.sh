#!/usr/bin/env bash

MYAPPNAME="SplunkModularInput"
PACKAGE="../../build/${MYAPPNAME}.tgz"
(cd ../etc/apps ; tar cvfz ${PACKAGE} ${MYAPPNAME})
exit