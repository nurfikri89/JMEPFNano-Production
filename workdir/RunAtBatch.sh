#!/bin/bash
#
#
#
export X509_USER_PROXY=/afs/cern.ch/user/n/nbinnorj/myProxy
cd ${JOBWORKDIR}
#
#
#
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
#
#
#
source RunNanoAODTest.sh ${1}
