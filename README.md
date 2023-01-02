# JMEPFNano-Production

Setup CMSSW release for the first time
```
mkdir AnaJMEPFNano; cd $_
cmsrel CMSSW_12_4_11_patch3
cd CMSSW_12_4_11_patch3/src
cmsenv
```
Checkout repository

```
git clone git@github.com:nurfikri89/JMEPFNano-Production.git JMEPFNano/Production
scram b -j4
cmsenv
```