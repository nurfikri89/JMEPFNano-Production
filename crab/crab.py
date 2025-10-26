############################################################
# Part 1
# - Setup common crab job configurations
#
############################################################
import CRABClient
from CRABClient.UserUtilities import config

crab_config = config()

#
# Config dir
#
configDir  = "configs/MiniToPFNanoV15_v1p0"

# configData =f'{configDir}/MiniToPFNanoV15_Data24_SkimHLTSingleMuon.py'
# configMC   =f'{configDir}/MiniToPFNanoV15_MC_RunIII2024Summer24_SkimHLTSingleMuon.py'
# tag        = "SkimHLTSingleMuon"

configData =f'{configDir}/MiniToPFNanoV15_Data24_SkimHLTDiMuon_AllCandsReducedInfo.py'
configMC   =f'{configDir}/MiniToPFNanoV15_MC_RunIII2024Summer24_SkimHLTDiMuon_AllCandsReducedInfo.py'
tag        = "SkimHLTDiMuon_AllCands"

#
# Set request name prefx
#
reqNamePrefix = f"MiniToPFNanoV15_v1p0"
#
# Set a non-empty string if we want to remake a sample but save in a new USER dataset
#
prodversion=""
# prodversion="-prodv2"
#
# Change this PATH where the crab directories are stored
# Example: config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects/'
#
# crab_config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects_pfnano/'
crab_config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects_pfnano_2/'

# crab_config.General.workArea = '/afs/cern.ch/work/n/nbinnorj/private/crab_projects_pfnano_v14/'
#
crab_config.JobType.pluginName = 'Analysis'

#
crab_config.Data.publication = True
crab_config.Data.allowNonValidInputDataset = True
crab_config.JobType.maxMemoryMB = 3000
crab_config.JobType.allowUndistributedCMSSW = True
#
# Specify the outLFNDirBase and your storage site
# JetMET CMS EOS space at CERN
#
# crab_config.Data.outLFNDirBase  = f'/store/group/phys_jetmet/{reqNamePrefix}/CRABOUTPUT/'
# crab_config.Site.storageSite    = 'T2_CH_CERN'
crab_config.Data.outLFNDirBase  = f'/store/user/nbinnorj/{reqNamePrefix}/CRABOUTPUT/'
crab_config.Site.storageSite    = 'T2_FI_HIP'
#
#
crab_config.Data.ignoreLocality = True
whitelist_sites=[
'T1_US_*',
'T1_ES_*',
'T1_IT_*',
'T1_FR_*',
'T1_RU_*',
'T1_DE_*',
'T2_US_*',
'T2_UK_*',
'T2_RU_*',
'T2_DE_*',
'T2_FR_*',
'T2_CH_*',
'T2_IT_*',
'T2_IN_*',
'T2_ES_*',
'T2_HU_*',
'T2_BE_*',
'T2_BR_*',
'T2_CN_*',
'T2_EE_*',
'T2_TW_*',
'T2_FI_*',
]
crab_config.Site.whitelist = whitelist_sites

############################################################
# Part 2
# -  Loop over list of samples. Send to Grid
#
############################################################
import sys
import helpers
from CRABAPI.RawCommand import crabCommand

runTime_data = 600
runTime_mc   = 600

fileSplit_data = 3
fileSplit_mc   = 2

#
# Read in txt file with list of samples
#
f = open(sys.argv[1]) 
samplelist =  helpers.GetSampleList(f)

#
# Print out the list of samples
#
print("Will send crab jobs for the following samples:")
for dataset in samplelist:
  print(dataset)
print("\n\n")

#
# For each sample, set crab job configuration and then send to the Grid
#
for i, dataset in enumerate(samplelist):
  print("%d/%d:Sending CRAB job: %s" % (i+1,len(samplelist), dataset))
  #
  # Specify input dataset
  #
  crab_config.Data.inputDataset = dataset
  #
  # FileBased split
  #
  crab_config.Data.splitting = 'FileBased'
  #
  # Check if Data or MC and use the appropriaet psetName
  #
  isData = helpers.IsSampleData(dataset)
  if isData:
    if "Run2024" in dataset and "MINIv6NANOv15" in dataset:
      crab_config.JobType.psetName = configData
      crab_config.Data.lumiMask = "../data/lumi/Cert_Collisions2024_378981_386951_Golden.json"
    crab_config.JobType.maxJobRuntimeMin = runTime_data
    crab_config.Data.unitsPerJob = fileSplit_data
    #
    # Have to make unique requestName.
    #
    primaryName   = dataset.split('/')[1]
    secondaryName = helpers.TrimSecondaryNameForData(dataset)
  else:
    if "RunIII2024Summer24MiniAODv6" in dataset:
      crab_config.JobType.psetName = configMC
    crab_config.JobType.maxJobRuntimeMin = runTime_mc
    crab_config.Data.unitsPerJob = fileSplit_mc
    #
    # Have to make unique requestName.
    #
    primaryName   = helpers.TrimPrimaryNameForMC(dataset)
    secondaryName = helpers.TrimSecondaryNameForMC(dataset)

  requestName = f"{primaryName}_{secondaryName}_{tag}_{reqNamePrefix}"
  if prodversion != "":
    requestName += prodversion
  crab_config.General.requestName = requestName

  outputDatasetTag = f"{secondaryName}_{tag}_{reqNamePrefix}"
  if prodversion != "":
    outputDatasetTag += prodversion
  crab_config.Data.outputDatasetTag = outputDatasetTag

  print("requestName: "+crab_config.General.requestName)
  print("outputDatasetTag: "+crab_config.Data.outputDatasetTag)
  print(crab_config.Data.splitting)
  print(crab_config.Data.unitsPerJob)
  print(crab_config.JobType.maxJobRuntimeMin)
  #####print(crab_config.Data.lumiMask)
  crabCommand('submit', config = crab_config)
  print("")
