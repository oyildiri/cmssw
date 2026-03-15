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
cmsRun /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test/testCPU_PU200_tkwt0p25.py inputFiles=root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_15_0_0/RelValUpsilon1SToMuMu_14/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v3/2580000/92b99ea5-e995-40fa-a8b9-9cd38fefa77f.root outputFile=/eos/user/o/oyildiri/OldNewCF/Upsilon/new2CnewF/outputfiles/run_1/92b99ea5-e995-40fa-a8b9-9cd38fefa77f_output.root
echo 'STOP---------------'
echo
echo
