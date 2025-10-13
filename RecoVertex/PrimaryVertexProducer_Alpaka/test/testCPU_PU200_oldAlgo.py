import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'output.root'
options.inputFiles = ['input.root']
options.maxEvents = -1 # -1 means all events
options.parseArguments()

process = cms.Process('PV',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('HLTrigger.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('commons_cff') 
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun3_2023_realistic_v3')

# Input files
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:/eos/cms/store/relval/CMSSW_15_0_0_pre2/RelValTTbar_14TeV/GEN-SIM-RECO/142X_mcRun3_2025_realistic_v4_RV266_RecoOnly_2025_noPU_Baseline-v1/2580000/6e617341-689b-454f-be4a-e898a8e3cbf6.root'#'/store/relval/CMSSW_15_0_0_pre2/RelValTTbar_14TeV/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v1/2590000/253f8a7f-1a05-4ae8-9065-5cff6b69b175.root',
    #),
    fileNames = cms.untracked.vstring(options.inputFiles), #'/store/relval/CMSSW_15_0_0_pre2/RelValTTbar_14TeV/GEN-SIM-RECO/PU_141X_mcRun4_realistic_v3_STD_Run4D110_PU-v1/2590000/253f8a7f-1a05-4ae8-9065-5cff6b69b175.root'),

    secondaryFileNames = cms.untracked.vstring(),
    #firstEvent=cms.untracked.uint32(10),
    #skipEvents = cms.untracked.uint32(9),
)

# Number of events to run
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
)

# Production metadata
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('PV nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.output = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(options.outputFile), # output file name
    outputCommands = cms.untracked.vstring('drop *','keep *_*_*_PV', 'keep *_genPUProtons_*_*', 'drop *_tpClusterProducer_*_*'),# I.e., just drop everything and keep things in this module
    splitLevel = cms.untracked.int32(0)
)

# Endpath and output
#process.endjob_step = cms.EndPath(process.endOfProcess)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)


################################
## Now the plugins themselves ##
################################


from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices

process.offlinePrimaryVertices = offlinePrimaryVertices
process.offlinePrimaryVertices.TkClusParameters.TkDAClusParameters.runInBlocks = cms.bool(False)
process.offlinePrimaryVertices.TkClusParameters.TkDAClusParameters.block_size = cms.uint32(512)
process.offlinePrimaryVertices.TkClusParameters.TkDAClusParameters.overlap_frac = cms.double(0.5)
process.offlinePrimaryVertices.vertexCollections = cms.VPSet(
       [cms.PSet(label=cms.string(""),
               algorithm=cms.string("AdaptiveVertexFitter"),
               chi2cutoff = cms.double(2.5),
               minNdof=cms.double(0.0),
               useBeamConstraint = cms.bool(False),
               maxDistanceToBeam = cms.double(1.0)
               ),
        cms.PSet(label=cms.string("WithBS"),
               algorithm = cms.string('AdaptiveVertexFitter'),
               chi2cutoff = cms.double(2.5),
               minNdof=cms.double(2.0),
               useBeamConstraint = cms.bool(True),
               maxDistanceToBeam = cms.double(1.0),
               )
        ])

process.options.wantSummary = True

##DQM Output step
process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(options.outputFile.replace(".root","_DQM.root")),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)


###################################
## Last, organize paths and exec ##
###################################

process.vertexAnalysis.vertexRecoCollections  = cms.VInputTag("offlinePrimaryVertices")
process.pvMonitor.vertexLabel = cms.InputTag("offlinePrimaryVertices")

process.tracksValidationTruth = cms.Task(process.VertexAssociatorByPositionAndTracks, process.quickTrackAssociatorByHits, process.tpClusterProducer)
process.pvValidation = cms.Sequence(process.vertexAnalysis,process.tracksValidationTruth)
process.prevalidation_step = cms.Path(process.pvValidation)

process.DQMOfflineVertex = cms.Sequence(process.pvMonitor)
process.dqmoffline_step = cms.EndPath(process.DQMOfflineVertex)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

process.vertexing_step = cms.Path(process.offlinePrimaryVertices)
process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(process.vertexing_step,process.prevalidation_step,process.dqmoffline_step,process.DQMoutput_step,process.output_step)

#process.vertexing_task = cms.EndPath(process.offlinePrimaryVertices)
#process.schedule = cms.Schedule(process.vertexing_task)
#process.schedule.extend([process.endjob_step,process.FEVToutput_step])
