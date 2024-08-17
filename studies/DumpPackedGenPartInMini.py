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

XROOTD="root://xrootd-cms.infn.it/"
# inputFiles=[
#   "/store/mc/Run3Summer23MiniAODv4/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/castor_130X_mcRun3_2023_realistic_v14-v1/2560000/7f7c0e56-590b-4f35-be6a-0bfafcc18b48.root"
# ]
# inputFilesFinal = [XROOTD+f for f in inputFiles]

inputFilesFinal = ["/afs/cern.ch/work/n/nbinnorj/Samples/Mini/store/mc/Run3Summer23MiniAODv4/QCD_PT-15to7000_TuneCP5_Flat2022_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v15-v3/2550000/7e2c2abe-4068-4e0d-802b-480acb242d32.root"]
print(inputFilesFinal[0])

handle_packedGenParts, label_packedGenParts = Handle("std::vector<pat::PackedGenParticle>"), "packedGenParticles"


def isAncestor(a,p) :
  if a == p :
    return True
  for i in xrange(0,p.numberOfMothers()) :
    if isAncestor(a,p.mother(i)) :
      return True
  return False

def analyseEvent(events, ievent):
  events.to(ievent)

  events.getByLabel (label_packedGenParts, handle_packedGenParts)
  packedGenParts = handle_packedGenParts.product()

  for ip in range(0,packedGenParts.size()):
    p = packedGenParts[ip]
    if abs(p.pdgId()) > 1000000000:
      print(f"PdgId : {p.pdgId()}  pt : {p.pt():<+.2f}  eta : {p.eta():<+.4f}  phi : {p.phi():<+.4f}")

events = Events(inputFilesFinal[0])
print(events.size())

nEvents = events.size()

maxEvent = -1
for iEvt in range(0,nEvents):
  if iEvt % 100 == 0:
    print(f"{iEvt} / {nEvents}")
  if maxEvent > 0 and iEvt+1 == maxEvent: break
  analyseEvent(events, iEvt)