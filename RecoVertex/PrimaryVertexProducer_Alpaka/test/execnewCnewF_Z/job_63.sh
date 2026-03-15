#!/bin/sh
echo
echo
echo 'START---------------'
echo 'WORKDIR ' ${PWD}
export HOME=$PWD
export X509_USER_PROXY=${proxy_path}
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test
cmsenv
cmsRun /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test/testCPU_PU200.py inputFiles=root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_15_0_0/RelValZMM_14/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v3/2580000/55f98f14-a7d1-4322-a320-ddb74cf5fb6f.root outputFile=/eos/user/o/oyildiri/OldNewCF/Z/newCnewF/outputfiles/run_3/55f98f14-a7d1-4322-a320-ddb74cf5fb6f_output.root
echo 'STOP---------------'
echo
echo
