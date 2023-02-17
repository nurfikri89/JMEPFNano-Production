# JMEPFNano-Production 

To setup the base for `v2p0_PuppiV17` production, setup CMSSW release for the first time

```
mkdir AnaJMEPFNano; cd $_
cmsrel CMSSW_12_6_4
cd CMSSW_12_6_4/src
cmsenv
git cms-init
```
then merge a branch to fix PileupJetId input variable calculation (soon to be included in `12_6_X`)

```
git cms-rebase-topic --old-base CMSSW_13_0_0_pre4 nurfikri89:portFrom131XTo1264_pujetid_fix
```

Checkout this repository

```
git clone git@github.com:nurfikri89/JMEPFNano-Production.git JMEPFNano/Production
scram b -j4
cmsenv
```
