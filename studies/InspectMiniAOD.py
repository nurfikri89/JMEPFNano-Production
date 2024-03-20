#
# python3 InspectMiniAOD.py
#
from builtins import range
import ROOT
ROOT.gROOT.SetBatch()
import sys
from DataFormats.FWLite import Events, Handle

# use single file name
# inFile="root://xrootd-cms.infn.it/" 

inFile="/afs/cern.ch/work/n/nbinnorj/Samples/Mini"
inFile+="/store/mc/Run3Summer22MiniAODv4/DYto2TautoMuTauh_M-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5-v2/30000/61952197-a800-4762-801a-152caf752be8.root"

print(inFile) 
events = Events (inFile)

# create handle outside of loop
handle  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag

# create handle outside of loop
handle_ak4chs,   label_ak4chs   = Handle ("std::vector<pat::Jet>"), "slimmedJets"
handle_ak4puppi, label_ak4puppi = Handle ("std::vector<pat::Jet>"), "slimmedJetsPuppi"
handle_ak8puppi, label_ak8puppi = Handle ("std::vector<pat::Jet>"), "slimmedJetsAK8"
handle_tau, label_tau           = Handle ("std::vector<pat::Tau>"), "slimmedTaus"

doPrintJetsAK4CHS=False
doPrintJetsAK4Puppi=False
doPrintJetsAK8Puppi=False
doPrintTau=True

# loop over events
for iEvt, event in enumerate(events):

  if iEvt == 100: break
  #
  #
  #
  def LoopOverJets(jets):
    njets = len(jets)
    for ijet in range(0, njets):
      print("ijet="+str(ijet))
      j = jets[ijet]
      print(f"{j.pt()=:.3f}, {j.eta()=:.3f}")
      # chEmEF = j.chargedEmEnergyFraction()
      # neEmEF = j.neutralEmEnergyFraction()
      # eleMult = j.electronMultiplicity()
      # phoMult = j.photonMultiplicity()
      # sigmaEtaEta = j.userFloat('hfJetShowerShape:sigmaEtaEta')
      # print("sigmaEtaEta = %.4f"%(sigmaEtaEta))
      # print("chEmEF = %.4f, neEmEF = %.4f, eta = %.4f"%(chEmEF, neEmEF, j.eta()))
      # print("   ele = %d, pho = %d,"%(eleMult, phoMult))
      # print("userDataNames")
      # userDataNames = j.userDataNames()
      # print("n="+str(userDataNames.size()))
      # for n in userDataNames:
      #     print(n)
      #
      # print("userFloatNames")
      # userFloatNames = j.userFloatNames()
      # print("n="+str(userFloatNames.size()))
      # for n in userFloatNames:
      #   print(n)
      #
      # print("userIntNames")
      # userIntNames = j.userIntNames()
      # print("n="+str(userIntNames.size()))
      # for n in userIntNames:
      #   print(n)

      ######################
      # For b-tagging names.
      ######################
      #
      # NOTE: Seems it is empty.
      #
      # print("tagInfoLabels")
      # tagInfoLabels = j.tagInfoLabels()
      # print("n="+str(tagInfoLabels.size()))
      # for n in tagInfoLabels:
      #     print(n)
      #
      # NOTE: This works
      #
      print("getPairDiscri")
      pairDiscri = j.getPairDiscri()
      print("n="+str(pairDiscri.size()))
      for disc in pairDiscri:
        print(f"{disc[0]} =  {j.bDiscriminator(disc[0]):.6f}")
      break
      print("\n")

  if doPrintJetsAK4CHS:
    event.getByLabel (label_ak4chs, handle_ak4chs)
    jets_ak4chs = handle_ak4chs.product()# get the product
    njets_ak4chs = len(jets_ak4chs)
    LoopOverJets(jets_ak4chs)

  if doPrintJetsAK4Puppi:
    event.getByLabel (label_ak4puppi, handle_ak4puppi)
    jets_ak4puppi = handle_ak4puppi.product()# get the product
    njets_ak4puppi = len(jets_ak4puppi)
    LoopOverJets(jets_ak4puppi)

  if doPrintJetsAK8Puppi:
    event.getByLabel (label_ak8puppi, handle_ak8puppi)
    jets_ak8puppi = handle_ak8puppi.product()# get the product
    njets_ak8puppi = len(jets_ak8puppi)
    LoopOverJets(jets_ak8puppi)

  #
  #
  #
  def LoopOverTaus(taus):
    ntaus = len(taus)
    for itau in range(0, ntaus):
      t = taus[itau]
      signalCands = t.signalCands()
      nSignalCands = signalCands.size()
      isoCands = t.isolationCands()
      nIsoCands = isoCands.size()
      nCandPtrs = t.numberOfSourceCandidatePtrs()
      print(f"{itau} : {t.isPFTau()=} : {t.decayMode()=} : {nSignalCands=} : {nCandPtrs=} : {nIsoCands=}")
      for iCand in range(0, nCandPtrs):
        cand = signalCands[iCand];
        print(f"SigCands   {iCand=}/{nSignalCands}, {cand.pt()=:.4f}, {cand.eta()=:.4f}, {cand.pdgId()=}")
      for iCand in range(0, nCandPtrs):
        cand = t.sourceCandidatePtr(iCand);
        print(f"SrcCandPtr {iCand=}/{nCandPtrs}, {cand.pt()=:.4f}, {cand.eta()=:.4f}, {cand.pdgId()=}")
      for iCand in range(0, nIsoCands):
        cand =isoCands[iCand];
        print(f"IsoCand    {iCand=}/{nIsoCands}, {cand.pt()=:.4f}, {cand.eta()=:.4f}, {cand.pdgId()=}")
      print("\n")
  if doPrintTau:
    event.getByLabel(label_tau, handle_tau)
    taus = handle_tau.product()# get the product
    print(len(taus))
    LoopOverTaus(taus)


