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
cmsRun /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test/testCPU_PU200_tkwt0p25.py inputFiles=root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_15_0_0/RelValVBFHZZ4Nu_14TeV/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v3/2580000/a8a62f7f-ba01-4742-b8b1-3754ab356f0d.root outputFile=/eos/user/o/oyildiri/OldNewCF/VBFHInv/new2CnewF/outputfiles/run_1/a8a62f7f-ba01-4742-b8b1-3754ab356f0d_output.root
echo 'STOP---------------'
echo
echo
