# JMEPFNano-Production

Setup CMSSW release for the first time
```
mkdir AnaJMEPFNano; cd $_
cmsrel CMSSW_13_2_6_patch1
cd CMSSW_13_2_6_patch1/src
cmsenv
```
Checkout repository

```
git clone git@github.com:nurfikri89/JMEPFNano-Production.git JMEPFNano/Production
scram b -j4
cmsenv
```
