#! /usr/bin/env python3 -u
import ROOT
import sys
import copy
import argparse
import pickle
from glob import glob
from DataFormats.FWLite import Events, Handle
# Allow loading CMSSW classes
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')

# https://github.com/cms-sw/cmssw/blob/CMSSW_13_0_13/PhysicsTools/HeppyCore/python/utils/deltar.py
# from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet
# from ProcessSampleHelpers import createHisto
# from ProcessSampleHelpers import bookIntBranch, bookFloatArrayBranch, bookDoubleArrayBranch
# from ProcessSampleHelpers import matchObjectCollection3
inputFilesFinal = ["/afs/cern.ch/work/n/nbinnorj/Samples/Mini/store/mc/Run3Summer22MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5_ext1-v2/2520000/d87515e2-a285-4ea5-8715-98a044ec5fc9.root"]
print(inputFilesFinal[0])

handle_slimmedElectrons = Handle("std::vector<pat::Electron>")
handle_slimmedPhotons = Handle("std::vector<pat::Photon>")
handle_slimmedMuons = Handle("std::vector<pat::Muon>")
handle_packedPFCandidates = Handle("std::vector<pat::PackedCandidate>")

def analyseEvent(events, iEvt):
  events.to(iEvt)

  # events.getByLabel ("slimmedElectrons", handle_slimmedElectrons)
  # slimmedElectrons = handle_slimmedElectrons.product()
  # for iEl in range(0,slimmedElectrons.size()):
  #   el = slimmedElectrons[iEl]
  #   print(f"el | {el.pt()} | {el.isPF()}")
  #   for pf in el.associatedPackedPFCandidates():
  #     print(f"   {pf.key()} | {pf.pt()} | {pf.pdgId()}")


  # events.getByLabel ("slimmedPhotons", handle_slimmedPhotons)
  # slimmedPhotons = handle_slimmedPhotons.product()
  # for iPho in range(0,slimmedPhotons.size()):
  #   pho = slimmedPhotons[iPho]
  #   print(f"pho | {pho.pt()} | {pho.eta()} | {pho.phi()}")
  #   for pf in pho.associatedPackedPFCandidates():
  #     print(f"   {pf.key()} | {pf.pt()} | {pf.eta()} | {pf.phi()} | {pf.pdgId()}")


  events.getByLabel ("packedPFCandidates", handle_packedPFCandidates)
  packedPFCandidates = handle_packedPFCandidates.product()

  # events.getByLabel ("slimmedMuons", handle_slimmedMuons)
  # slimmedMuons = handle_slimmedMuons.product()
  # for iMu in range(0,slimmedMuons.size()):
  #   mu = slimmedMuons[iMu]
  #   print(f"mu | {mu.pt():.2f} | {mu.eta():.4f} | {mu.phi():.4f} | {mu.isPFMuon()}")
  #   for ipf in range(0,mu.numberOfSourceCandidatePtrs()):
  #     pfkey = mu.sourceCandidatePtr(ipf).key()
  #     print(pfkey)
  #     if pfkey >= 0:
  #       pf = packedPFCandidates[pfkey]
  #       print(f" {pf.pt():.2f} | {pf.eta():.4f} | {pf.phi():.4f} | {pf.pdgId()}")
  #   print("\n")

  events.getByLabel ("slimmedElectrons", handle_slimmedElectrons)
  slimmedElectrons = handle_slimmedElectrons.product()
  for iEl in range(0,slimmedElectrons.size()):
    el = slimmedElectrons[iEl]
    print(f"el | {el.pt():.2f} | {el.eta():.4f} | {el.phi():.4f}  | {el.isPF()}")
    for ipf in range(0,el.numberOfSourceCandidatePtrs()):
      pfkey = el.sourceCandidatePtr(ipf).key()
      print(pfkey)
      if pfkey >= 0:
        pf = packedPFCandidates[pfkey]
        print(f" {pf.pt():.2f} | {pf.eta():.4f} | {pf.phi():.4f} | {pf.pdgId()}")
  print("\n")

events = Events(inputFilesFinal[0])
print(events.size())

nEvents = events.size()

maxEvent = -1
for iEvt in range(0,nEvents):
  if iEvt % 100 == 0:
    print(f"{iEvt} / {nEvents}")
  if maxEvent > 0 and iEvt+1 == maxEvent: break
  analyseEvent(events, iEvt)