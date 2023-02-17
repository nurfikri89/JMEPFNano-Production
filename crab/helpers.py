def GetSampleList(file):
  samplelist = file.readlines()
  samplelist = [x.strip() for x in samplelist] 
  samplelist = [x for x in samplelist if x] # Choose lines that are not empty
  samplelist = [x for x in samplelist if not(x.startswith("#"))] # Choose lines that do not start with #
  return samplelist

def TrimPrimaryNameForMC(dataset):
  name = dataset.split('/')[1]
  name = name.replace("_13TeV","")
  name = name.replace("_13p6TeV","")
  name = name.replace("_TuneCP5","")
  name = name.replace("pythia","py")
  name = name.replace("herwig","hw")
  name = name.replace("madgraph","mg")
  name = name.replace("powheg","phg")
  name = name.replace("amcatnlo","mcNLO")
  name = name.replace("powhegMiNNLO","pwhg")
  name = name.replace("-photos","")
  name = name.replace("FXFX","")
  name = name.replace("_MatchEWPDG20","")
  return name

def TrimSecondaryNameForMC(dataset):
  name = dataset.split('/')[2]
  name = name.replace("RunIISummer20UL18MiniAODv2-","MCUL18MiniAODv2")#RENAME CAMPAIGN.
  name = name.replace("106X_upgrade2018_realistic_v16_L1v1","") #REMOVE GT.
  name = name.replace("Run3Summer22MiniAODv3-","MC22MiniAODv3")#RENAME CAMPAIGN.
  name = name.replace("124X_mcRun3_2022_realistic_v12","") #REMOVE GT.
  name = name.replace("Run3Summer22EEMiniAODv3-","MC22EEMiniAODv3")#RENAME CAMPAIGN.
  name = name.replace("124X_mcRun3_2022_realistic_postEE_v1","") #REMOVE GT.
  name = name.replace("-v1","")# 
  name = name.replace("-v2","")# 
  name = name.replace("-v3","")#
  name = name.replace("-v4","")# Remove any version indication.There should only be one valid version for MC samples
  return name

def TrimSecondaryNameForData(dataset):
  name = dataset.split('/')[2]
  #
  # Note: For PromptReco, we do need the version as different versions 
  # means different run number ranges.
  #
  # name = name.replace("-v1","")# 
  # name = name.replace("-v2","")# 
  # name = name.replace("-v3","")#
  # name = name.replace("-v4","")# Remove any version indication.
  return name

def IsSampleData(dataset):
  name = dataset.split('/')[2]
  isData = False
  if   "Run2022" in name:isData = True
  if   "Run2018" in name:isData = True
  if   "Run2017" in name:isData = True
  if   "Run2016" in name:isData = True
  return isData

