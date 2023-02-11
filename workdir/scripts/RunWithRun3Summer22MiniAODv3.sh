NEVENTS=100
GT=126X_mcRun3_2022_realistic_v2
ERA=Run3,run3_nanoAOD_124

### INFILEPREFIX=/afs/cern.ch/work/n/nbinnorj/Samples/Mini/
INFILEPREFIX=root://xrootd-cms.infn.it/

#
# QCD sample
#
INFILE=${INFILEPREFIX}/store/mc/Run3Summer22MiniAODv3/QCD_PT-15_TuneCP5_Flat2018_13p6TeV_pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v2/30000/1ad67ce0-b03e-4d8b-ac68-03eb4a32e2ef.root
OUTFILE=tree_jmepfnano_qcd.root
CFGFILE=./JME-Run3Summer22NanoAOD_JMEPFNano_qcd.py

#
# TT sample 
#
# INFILE=${INFILEPREFIX}/store/mc/Run3Summer22MiniAODv3/TT_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v3/70000/ac3541ad-110b-4273-9827-99298b27dd67.root
# OUTFILE=tree_jmepfnano_tt.root
# CFGFILE=./JME-Run3Summer22NanoAOD_JMEPFNano_tt.py

#
# run JMEPFNano 
#
CUSTOMISE_COMMAND="from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)\n"

#
# run JMEPFNano with puppi recomputed
#
# CUSTOMISE_COMMAND="from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)\n"
# CUSTOMISE_COMMAND+="process.packedPFCandidatespuppi.useExistingWeights=False\n"

#
# just run JMENano
#
# CUSTOMISE_COMMAND="from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)\n "

cmsDriver.py step1 \
--mc \
--filein=file:${INFILE} \
--fileout=file:${OUTFILE} \
--step NANO \
--eventcontent NANOAODSIM \
--datatier NANOAODSIM \
--conditions ${GT} \
--era ${ERA} \
--python_filename ${CFGFILE}  \
--no_exec \
-n ${NEVENTS} \
--customise_commands="${CUSTOMISE_COMMAND}"


