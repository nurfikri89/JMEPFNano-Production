#!/bin/bash

SAMPLE=${1}

# NOF_EVENTS=50
NOF_EVENTS=100
# NOF_EVENTS=250
# NOF_EVENTS=500
# NOF_EVENTS=1000
# NOF_EVENTS=2000
# NOF_EVENTS=5000
# NOF_EVENTS=10000

CUSTOMISE_COMMAND_MC=""
CUSTOMISE_COMMAND_DATA=""

CUSTOMISE_MC=""
CUSTOMISE_DATA=""

TAG="customjmepfnano_default"

CUSTOMISE_COMMAND_MC="from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)\n"
CUSTOMISE_COMMAND_DATA="from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_Data; PrepJMEPFCustomNanoAOD_Data(process)\n"

# TAG="customjmenano_default"
# CUSTOMISE_COMMAND_MC="from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)\n"
# CUSTOMISE_COMMAND_DATA="from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_Data; PrepJMECustomNanoAOD_Data(process)\n"

mkdir -p ./dir_cfg_${TAG}/
mkdir -p ./dir_log_${TAG}/
mkdir -p ./dir_output_${TAG}/
############################################
#
# Set Global Tag depending on CMSSW version
#
############################################
if [[ $CMSSW_VERSION == *"CMSSW_13_0_"* ]]; then
  echo "Using CMSSW_13_0_X GT"
  GT_MC_2022="auto:phase1_2022_realistic"
  GT_MC_2018=auto:phase1_2018_realistic
  GT_MC_2017=auto:phase1_2017_realistic
  GT_MC_2016=auto:run2_mc
  GT_MC_2016APV=auto:run2_mc
  GT_DATA_2022=auto:run3_data
  GT_DATA_2018=auto:run2_data
  GT_DATA_2017=auto:run2_data
  GT_DATA_2016=auto:run2_data
  GT_DATA_2016APV=auto:run2_data
elif [[ $CMSSW_VERSION == *"CMSSW_12_6_"* ]]; then
  echo "Using CMSSW_12_6_X GT"
  GT_MC_2022="auto:phase1_2022_realistic"
  GT_MC_2018=auto:phase1_2018_realistic
  GT_MC_2017=auto:phase1_2017_realistic
  GT_MC_2016=auto:run2_mc
  GT_MC_2016APV=auto:run2_mc
  GT_DATA_2022=auto:run3_data
  GT_DATA_2018=auto:run2_data
  GT_DATA_2017=auto:run2_data
  GT_DATA_2016=auto:run2_data
  GT_DATA_2016APV=auto:run2_data
elif [[ $CMSSW_VERSION == *"CMSSW_12_4_"* ]]; then
  echo "Using CMSSW_12_4_X GT"
  GT_MC_2022="auto:phase1_2022_realistic"
  GT_MC_2018=auto:phase1_2018_realistic
  GT_MC_2017=auto:phase1_2017_realistic
  GT_MC_2016=auto:run2_mc
  GT_MC_2016APV=auto:run2_mc
  GT_DATA_2022=auto:run3_data
  GT_DATA_2018=auto:run2_data
  GT_DATA_2017=auto:run2_data
  GT_DATA_2016=auto:run2_data
  GT_DATA_2016APV=auto:run2_data
elif [[ $CMSSW_VERSION == *"CMSSW_10_6_"* ]]; then
  # Always check
  # https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis
  echo "Using CMSSW_10_6_X GT"
  GT_MC_2018=106X_upgrade2018_realistic_v16_L1v1 #NanoAODv9 GT
  GT_MC_2017=106X_mc2017_realistic_v9    #NanoAODv9 GT
  GT_MC_2016=106X_mcRun2_asymptotic_v17  #NanoAODv9 GT
  GT_MC_2016APV=106X_mcRun2_asymptotic_preVFP_v11  #NanoAODv9 GT
  GT_DATA_2018=106X_dataRun2_v35 #NanoAODv9 GT
  GT_DATA_2017=106X_dataRun2_v35 #NanoAODv9 GT
  GT_DATA_2016=106X_dataRun2_v35 #NanoAODv9 GT
  GT_DATA_2016APV=106X_dataRun2_v35 #NanoAODv9 GT
  #
  # Use this customise command
  #
  CUSTOMISE_COMMAND_MC="from JMEPFNano.Production.custom_jme_pf_nano_10630_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)\n"
  CUSTOMISE_COMMAND_DATA="from JMEPFNano.Production.custom_jme_pf_nano_10630_cff import PrepJMEPFCustomNanoAOD_Data; PrepJMEPFCustomNanoAOD_Data(process)\n"
else
  echo "Cannot recognize CMSSW version: ${CMSSW_VERSION}"
  echo "GT not set. Stopping bash script now"
  return
fi  

INFILEPREFIX="/afs/cern.ch/user/n/nbinnorj/work/Samples/Mini"
# INFILEPREFIX="root://xrootd-cms.infn.it/"
#######################################
#
# UL MC MiniAODv2
#
########################################
if [ $SAMPLE == 'MCUL18V2_QCD' ]; then
  GT=$GT_MC_2018
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/62E879B1-359D-E348-B2E8-36568A135395.root"
  NANOAOD="tree_MCUL18_miniV2_qcd.root"
  NANOAOD_CFG=JME-RunIISummer20UL18NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2018,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL18_miniV2.log"
elif [ $SAMPLE == 'MCUL18V2_TTToHadronic' ]; then
  GT=$GT_MC_2018
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/100000/1F5F2A97-334A-A249-85D3-9AB5F1268838.root"
  NANOAOD="tree_MCUL18_miniV2_tthadronic.root"
  NANOAOD_CFG=JME-RunIISummer20UL18NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2018,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL18_miniV2.log"
elif [ $SAMPLE == 'MCUL18V2_DYJetsToLL' ]; then
  GT=$GT_MC_2018
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL18MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1_ext1-v1/50000/99327950-C31C-9341-BA87-BAC5C7988F14.root"
  NANOAOD="tree_MCUL18_miniV2_dyjetstoll.root"
  NANOAOD_CFG=JME-RunIISummer20UL18NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2018,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL18_miniV2.log"
elif [ $SAMPLE == 'MCUL18V2' ]; then
  GT=$GT_MC_2018
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL18MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/270000/F3DBDA07-9E4B-0245-B618-54B67ED34DB4.root"
  NANOAOD="tree_MCUL18_miniV2_ttjets.root"
  NANOAOD_CFG=JME-RunIISummer20UL18NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2018,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL18_miniV2.log"
elif [ $SAMPLE == 'MCUL17V2' ]; then
  GT=$GT_MC_2017
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/C7153D76-622D-C744-9D93-626062F46EFA.root"
  NANOAOD="tree_MCUL17_miniV2_ttjets.root"
  NANOAOD_CFG=JME-RunIISummer20UL17NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2017,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL17_miniV2.log"
elif [ $SAMPLE == 'MCUL16V2' ]; then
  GT=$GT_MC_2016
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL16MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/30000/BD0D6D63-8B3C-AC4A-8204-D4C2AA1733B5.root"
  NANOAOD="tree_MCUL16_miniV2_ttjets.root"
  NANOAOD_CFG=JME-RunIISummer20UL16NanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2016,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL16_miniV2.log"
elif [ $SAMPLE == 'MCUL16APVV2' ]; then
  GT=$GT_MC_2016APV
  MINIAOD=${INFILEPREFIX}"/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2540000/08FEA848-D3D8-3A4B-BEF2-BFD8BADE8263.root"
  NANOAOD="tree_MCUL16APV_miniV2_ttjets.root"
  NANOAOD_CFG=JME-RunIISummer20UL16APVNanoAOD_miniV2_${TAG}_cfg.py
  ERA="Run2_2016_HIPM,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_MCUL16APV_miniV2.log"
#######################################
#
# UL MC22
#
########################################
elif [ $SAMPLE == 'MC22_122_QCD' ]; then
  GT=$GT_MC_2022
  # /QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/Run3Winter22MiniAOD-122X_mcRun3_2021_realistic_v9-v2/MINIAODSIM
  MINIAOD=${INFILEPREFIX}"/store/mc/Run3Winter22MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/MINIAODSIM/122X_mcRun3_2021_realistic_v9-v2/40000/d1e21ec5-4f08-48a6-a471-26b94bcb1a25.root"
  NANOAOD="tree_MC22_mini_122_qcd.root"
  NANOAOD_CFG=JME-Run3Winter22NanoAOD_mini_122_qcd_${TAG}_cfg.py
  ERA="Run3,run3_nanoAOD_122"
  LOGFILE="nanoaod_MC22_mini_122_qcd.log"
elif [ $SAMPLE == 'MC22_122_TTTo2J1L1Nu' ]; then
  GT=$GT_MC_2022
  # /TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8/Run3Winter22MiniAOD-122X_mcRun3_2021_realistic_v9-v2/MINIAODSIM
  MINIAOD=${INFILEPREFIX}"/store/mc/Run3Winter22MiniAOD/TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8/MINIAODSIM/122X_mcRun3_2021_realistic_v9-v2/2550000/9dad1fae-b379-4ce8-936b-d1872db9c0ce.root"
  NANOAOD="tree_MC22_mini_122_tt1lep.root"
  NANOAOD_CFG=JME-Run3Winter22NanoAOD_mini_122_tt1lep_${TAG}_cfg.py
  ERA="Run3,run3_nanoAOD_122"
  LOGFILE="nanoaod_MC22_mini_122_tt1lep.log"
#######################################
#
# UL Data MiniAODv2
#
########################################
elif [ $SAMPLE == 'DATAUL18V2' ]; then 
  GT=$GT_DATA_2018
  MINIAOD=${INFILEPREFIX}"/store/data/Run2018D/JetHT/MINIAOD/UL2018_MiniAODv2-v1/280000/CEF1196D-17C4-0A4F-A62D-E0C2A0CCB857.root"
  NANOAOD="tree_DataUL18_2018D_miniV2_jetht.root"
  NANOAOD_CFG=JME-RunIIData18ULV2NanoAOD_${TAG}_cfg.py
  ERA="Run2_2018,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_DataUL18_miniV2.log"
elif [ $SAMPLE == 'DATAUL17V2' ]; then 
  GT=$GT_DATA_2017
  MINIAOD=${INFILEPREFIX}"/store/data/Run2017F/JetHT/MINIAOD/UL2017_MiniAODv2-v1/40000/05445FB8-AEF6-2F40-87F9-C1749F0A7B7E.root"
  NANOAOD="tree_DataUL17_2017F_miniV2_jetht.root"
  NANOAOD_CFG=JME-RunIIData17ULV2NanoAOD_${TAG}_cfg.py
  ERA="Run2_2017,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_DataUL17_miniV2.log"
elif [ $SAMPLE == 'DATAUL16V2' ]; then 
  GT=$GT_DATA_2016
  MINIAOD=${INFILEPREFIX}"/store/data/Run2016H/JetHT/MINIAOD/UL2016_MiniAODv2-v1/130000/08AFBF12-DAB5-EA45-B6FC-E8B08748ADE7.root"
  NANOAOD="tree_DataUL16_2016G_miniV2_jetht.root"
  NANOAOD_CFG=JME-RunIIData16ULV2NanoAOD_${TAG}_cfg.py
  ERA="Run2_2016,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_DataUL16_miniV2.log"
elif [ $SAMPLE == 'DATAUL16APVV2' ]; then 
  GT=$GT_DATA_2016APV
  MINIAOD=${INFILEPREFIX}"/store/data/Run2016E/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v1/280000/C42BD3A9-A504-F145-9034-4F77276AEA5B.root"
  NANOAOD="tree_DataUL16APV_2016E_miniV2_jetht.root"
  NANOAOD_CFG=JME-RunIIData16APVULV2NanoAOD_${TAG}_cfg.py
  ERA="Run2_2016_HIPM,run2_nanoAOD_106Xv2"
  LOGFILE="nanoaod_DataUL16APV_miniV2.log"
#######################################
#
# Run3 Data MiniAOD
#
########################################
elif [ $SAMPLE == 'DATA22' ]; then 
  GT=$GT_DATA_2022
  MINIAOD=${INFILEPREFIX}"/store/data/Run2022C/JetHT/MINIAOD/PromptReco-v1/000/355/913/00000/d2f9f454-431e-4cb8-8d99-cdd7b779fab6.root"
  NANOAOD="tree_DataUL22_2022C_mini_jetht.root"
  NANOAOD_CFG=JME-Run3Data22NanoAOD_${TAG}_cfg.py
  ERA="Run3,run3_nanoAOD_devel"
  LOGFILE="nanoaod_DataUL22_miniV2.log"
else
  echo "SAMPLE not recognised. You specified:"${SAMPLE}
  echo "STOPPING NOW"
  return
fi

########################################################################################
#
# Starting from 12_1_X, we can make those pretty
# profile pie charts. We have to add the following
# customization.
# https://github.com/fwyzard/circles
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/FastTimerService
# https://github.com/cms-sw/cms-bot/blob/master/reco_profiling/profileRunner.py#L87
#
########################################################################################
CUSTOM_TIMER=""
# if [[ $CMSSW_VERSION == *"CMSSW_12_5_"* ]]; then
#   CUSTOM_TIMER+="from HLTrigger.Timer.FastTimer import customise_timer_service_singlejob; customise_timer_service_singlejob(process) \n"
#   CUSTOM_TIMER+="process.FastTimerService.writeJSONSummary=True\n"
#   CUSTOM_TIMER+="process.FastTimerService.jsonFileName='./dir_log_${TAG}/resources_${SAMPLE}_${TAG}.json'\n"
#   echo ${CUSTOM_TIMER}
# elif [[ $CMSSW_VERSION == *"CMSSW_12_4_"* ]]; then
#   CUSTOM_TIMER+="from HLTrigger.Timer.FastTimer import customise_timer_service_singlejob; customise_timer_service_singlejob(process) \n"
#   CUSTOM_TIMER+="process.FastTimerService.writeJSONSummary=True\n"
#   CUSTOM_TIMER+="process.FastTimerService.jsonFileName='./dir_log_${TAG}/resources_${SAMPLE}_${TAG}.json'\n"
#   echo ${CUSTOM_TIMER}
# elif [[ $CMSSW_VERSION == *"CMSSW_12_3_"* ]]; then
#   CUSTOM_TIMER+="from HLTrigger.Timer.FastTimer import customise_timer_service_singlejob; customise_timer_service_singlejob(process) \n"
#   CUSTOM_TIMER+="process.FastTimerService.writeJSONSummary=True\n"
#   CUSTOM_TIMER+="process.FastTimerService.jsonFileName='./dir_log_${TAG}/resources_${SAMPLE}_${TAG}.json'\n"
#   echo ${CUSTOM_TIMER}
# elif [[ $CMSSW_VERSION == *"CMSSW_12_1_"* ]]; then
#   CUSTOM_TIMER+="from HLTrigger.Timer.FastTimer import customise_timer_service_singlejob; customise_timer_service_singlejob(process) \n"
#   CUSTOM_TIMER+="process.FastTimerService.writeJSONSummary=True\n"
#   CUSTOM_TIMER+="process.FastTimerService.jsonFileName='./dir_log_${TAG}/resources_${SAMPLE}_${TAG}.json'\n"
#   echo ${CUSTOM_TIMER}
# fi
CUSTOMISE_COMMAND_MC+=${CUSTOM_TIMER}
CUSTOMISE_COMMAND_DATA+=${CUSTOM_TIMER}


CUSTOM_LOGGER=""
# CUSTOM_LOGGER="process.MessageLogger.cerr.FwkReport.reportEvery = 1\n process.MessageLogger.cerr.threshold = \"INFO\""
CUSTOMISE_COMMAND_MC+=${CUSTOM_LOGGER}
CUSTOMISE_COMMAND_DATA+=${CUSTOM_LOGGER}

echo -e "\n\n"
echo "GT: "${GT}
echo "NANOAOD_CFG: "${NANOAOD_CFG}
echo "LOGFILE: "${LOGFILE}
echo "CUSTOMISE_MC: "${CUSTOMISE_MC}
echo "CUSTOMISE_DATA: "${CUSTOMISE_DATA}
echo "CUSTOMISE_COMMAND_MC: "${CUSTOMISE_COMMAND_MC}
echo "CUSTOMISE_COMMAND_DATA: "${CUSTOMISE_COMMAND_DATA}

if [[ (-z $CUSTOMISE_COMMAND_MC) && (-z $CUSTOMISE_COMMAND_DATA) && (-z $CUSTOMISE_MC) && (-z $CUSTOMISE_DATA) ]]; then
  #
  # Run without customization
  #
  # 
  echo "No customization"
  echo -e "\n\n"
  if [[ ${SAMPLE} == *"MC"* ]]; then
    echo "Producing a NANOAODSIM file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --mc \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_$TAG/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}"
  elif [[ ${SAMPLE} == *"DATA"* ]]; then
    echo "Producing a NANOAOD file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --data \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_${TAG}/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}"
  fi
elif [[ (! -z $CUSTOMISE_MC)  &&  (! -z $CUSTOMISE_DATA) && (! -z $CUSTOMISE_COMMAND_MC) && (! -z $CUSTOMISE_COMMAND_DATA)  ]]; then
  #
  # Run with --customise input and with --customise_commands
  #
  echo "With --customise"
  echo "and with --customise_commands"
  echo -e "\n\n"
  if [[ ${SAMPLE} == *"MC"* ]]; then
    echo "Producing a NANOAODSIM file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --mc \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_$TAG/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise="${CUSTOMISE_MC}" \
    --customise_commands="${CUSTOMISE_COMMAND_MC}"
  elif [[ ${SAMPLE} == *"DATA"* ]]; then
    echo "Producing a NANOAOD file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --data \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_${TAG}/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise="${CUSTOMISE_DATA}" \
    --customise_commands="${CUSTOMISE_COMMAND_DATA}"
  fi
elif [[ (! -z $CUSTOMISE_MC)  &&  (! -z $CUSTOMISE_DATA) ]]; then
  #
  # Run with --customise input
  #
  echo "With --customise"
  echo -e "\n\n"
  if [[ ${SAMPLE} == *"MC"* ]]; then
    echo "Producing a NANOAODSIM file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --mc \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_$TAG/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise="${CUSTOMISE_MC}"
  elif [[ ${SAMPLE} == *"DATA"* ]]; then
    echo "Producing a NANOAOD file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --data \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_${TAG}/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise="${CUSTOMISE_DATA}"
  fi
else
  #
  # Run with --customise_commands input
  #
  echo "With --customise_commands"
  echo -e "\n\n"
  if [[ ${SAMPLE} == *"MC"* ]]; then
    echo "Producing a NANOAODSIM file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --mc \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_$TAG/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise_commands="${CUSTOMISE_COMMAND_MC}"
  elif [[ ${SAMPLE} == *"DATA"* ]]; then
    echo "Producing a NANOAOD file ${NANOAOD} from ${MINIAOD}"
    cmsDriver.py step1 \
    --data \
    --fileout file:./dir_output_${TAG}/${NANOAOD} \
    --eventcontent NANOAODSIM \
    --datatier NANOAODSIM \
    --conditions ${GT} \
    --step NANO \
    --era ${ERA} \
    --python_filename ./dir_cfg_${TAG}/${NANOAOD_CFG} \
    --no_exec \
    -n ${NOF_EVENTS} \
    --filein="file:${MINIAOD}" \
    --customise_commands="${CUSTOMISE_COMMAND_DATA}"
  fi
fi

echo -e "\n\n\n\n"
echo "cmsRun ${NANOAOD_CFG}"
echo "Started at `date`"
cmsRun ./dir_cfg_${TAG}/${NANOAOD_CFG}  2>&1 | tee ./dir_log_${TAG}/${LOGFILE} 
echo "Finished at `date`"

# echo -e "\n\n\n\n"
# echo "cmsRun $NANOAOD_CFG"
# echo "Started at `date`"
# igprof -d -t cmsRun -pp -z -o ./dir_log_$TAG/igprof.output_cpu.${SAMPLE}_${TAG}.gz cmsRun ./dir_cfg_$TAG/$NANOAOD_CFG 2>&1 | tee ./dir_log_$TAG/${LOGFILE} 
# echo "Finished at `date`"

