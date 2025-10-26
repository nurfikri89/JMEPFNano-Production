
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_2023_cff import Run3_2023

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register('jobNumber',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,"jobNumber")
options.parseArguments()

process = cms.Process('NANO',Run3_2023)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

###########################################################################
#
# Follow logic in https://github.com/dmwm/CRABServer/blob/master/scripts/TweakPSet.py
#
###########################################################################
from ast import literal_eval
def readFileFromTarball(filename, tarball):
    import os
    import tarfile
    def decodeBytesToUnicode(value, errors="strict"):
        if isinstance(value, bytes):
            return value.decode("utf-8", errors)
        return value

    """ returns a string with the content of once file in a tarball """
    content = '{}'
    if os.path.isfile(filename):
        # This is only for Debugging
        print('DEBUGGING MODE!')
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return literal_eval(content)
    if not os.path.exists(tarball):
        raise RuntimeError(f"Error getting {tarball} file location")
    tarFile = tarfile.open(tarball)
    for member in tarFile.getmembers():  # pylint: disable=unused-variable
        try:
            f = tarFile.extractfile(filename)
            content = f.read()
            content = decodeBytesToUnicode(content)
            break
        except KeyError as er:
            # Don`t exit due to KeyError, print error. EventBased and FileBased does not have run and lumis
            print(f"Failed to get information from tarball {tarball} and file {filename}. Error : {er}")
            break
    tarFile.close()
    return literal_eval(content)

inputFileNameTxtFile = f"job_input_file_list_{options.jobNumber}.txt"
inputFiles = {}
inputFiles = readFileFromTarball(inputFileNameTxtFile, 'input_files.tar.gz')
print("inputFiles = ")
print(inputFiles)

primaryFiles = []
for inputFile in inputFiles:
    if not isinstance(inputFile, dict):
        inputFile = {'lfn': inputFile, 'parents': []}
    primaryFiles.append(inputFile["lfn"])

print("primaryFiles = ")
print(primaryFiles)
###########################################################################
#
#
###########################################################################

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(primaryFiles),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:treeForRuns.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_mcRun3_2023_realistic_v5', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon

#call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

process.NANOAODSIMoutput.outputCommands = cms.untracked.vstring(
    'drop *',
    'keep nanoaodFlatTable_genWeightsTable_*_*',
    'keep nanoaodMergeableCounterTable_genWeightsTable_*_*',
)
process.NANOAODSIMoutput.saveProvenance = cms.untracked.bool(False)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
