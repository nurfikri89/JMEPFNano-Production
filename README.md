# JMEPFNano-Production

Setup CMSSW release for the first time
```
mkdir AnaJMEPFNano; cd $_
cmsrel CMSSW_12_6_0_patch1
cd CMSSW_12_6_0_patch1/src
cmsenv
```
Checkout repository specifically this branch (`for1260patch1_JMENanoV11`)

```
git clone -b for1260patch1_JMENanoV11 git@github.com:nurfikri89/JMEPFNano-Production.git JMEPFNano/Production
scram b -j4
cmsenv
```
