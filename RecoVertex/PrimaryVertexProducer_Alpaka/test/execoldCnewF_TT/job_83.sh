#!/bin/sh
echo
echo
echo 'START---------------'
echo 'WORKDIR ' ${PWD}
export HOME=$PWD
export X509_USER_PROXY=/afs/cern.ch/user/o/oyildiri/private/x509up_u188570
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test
cmsenv
rm /eos/user/o/oyildiri/OldNewCF/TT/oldCnewF/outputfiles/run_2/f3a928c0-7f9e-4ed3-8463-bf48468688a2_output.root
rm /eos/user/o/oyildiri/OldNewCF/TT/oldCnewF/outputfiles/run_2/f3a928c0-7f9e-4ed3-8463-bf48468688a2_output_DQM.root
cmsRun /afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test/testCPU_PU200_oldCnewF.py inputFiles=root://cms-xrd-global.cern.ch//store/relval/CMSSW_15_0_0/RelValTTbar_14TeV/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v3/2580000/f3a928c0-7f9e-4ed3-8463-bf48468688a2.root outputFile=/eos/user/o/oyildiri/OldNewCF/TT/oldCnewF/outputfiles/run_2/f3a928c0-7f9e-4ed3-8463-bf48468688a2_output.root
echo 'STOP---------------'
echo
echo
