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
    #),
    fileNames = cms.untracked.vstring(options.inputFiles), 
    secondaryFileNames = cms.untracked.vstring(),
)

# Number of events to run
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents),
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

process.offlinePrimaryVertices4D = offlinePrimaryVertices

# Configure to use 2D clusterizer
process.offlinePrimaryVertices4D.TkClusParameters = cms.PSet(algorithm = cms.string("DA2D_vect"),
        TkDAClusParameters = cms.PSet(
            Tmin = cms.double(4.0),
            Tpurge = cms.double(4.0),
            Tstop = cms.double(2.0),
        )
)

# Add track timing
process.offlinePrimaryVertices4D.TrackTimesLabel = cms.InputTag("trackTimeValueMapProducer","generalTracksConfigurableFlatResolutionModel")
process.offlinePrimaryVertices4D.TrackTimeResosLabel = cms.InputTag("trackTimeValueMapProducer","generalTracksConfigurableFlatResolutionModelResolution")
process.offlinePrimaryVertices4D.trackMTDTimeQualityVMapTag = cms.InputTag("mtdTrackQualityMVA:mtdQualMVA")
process.offlinePrimaryVertices4D.useMVACut = cms.bool(False)
process.offlinePrimaryVertices4D.minTrackTimeQuality = cms.double(0.8)
process.offlinePrimaryVertices4D.vertexCollections = cms.VPSet(
     [cms.PSet(label=cms.string(""),
               algorithm=cms.string("AdaptiveVertexFitter"),
               chi2cutoff = cms.double(2.5),
               minNdof=cms.double(0.0),
               useBeamConstraint = cms.bool(False),
               maxDistanceToBeam = cms.double(1.0),
               vertexTimeParameters = cms.PSet( algorithm = cms.string('fromTracksPID')),
               ),
      cms.PSet(label=cms.string("WithBS"),
               algorithm = cms.string('AdaptiveVertexFitter'),
               chi2cutoff = cms.double(2.5),
               minNdof=cms.double(2.0),
               useBeamConstraint = cms.bool(True),
               maxDistanceToBeam = cms.double(1.0),
               vertexTimeParameters = cms.PSet( algorithm = cms.string('fromTracksPID')),
               )
      ]
)

#process.tofPID4DnoPID=tofPIDProducer.clone(vtxsSrc='unsortedOfflinePrimaryVertices')

process.offlinePrimaryVertices4DwithPID = process.offlinePrimaryVertices4D.clone(
    TrackTimesLabel = "tofPID:t0safe",
    TrackTimeResosLabel = "tofPID:sigmat0safe"
)

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

process.vertexAnalysis.vertexRecoCollections  = cms.VInputTag("offlinePrimaryVertices4D")
process.pvMonitor.vertexLabel = cms.InputTag("offlinePrimaryVertices4D")

process.tracksValidationTruth = cms.Task(process.VertexAssociatorByPositionAndTracks, process.quickTrackAssociatorByHits, process.tpClusterProducer)
process.pvValidation = cms.Sequence(process.vertexAnalysis,process.tracksValidationTruth)
process.prevalidation_step = cms.Path(process.pvValidation)

process.DQMOfflineVertex = cms.Sequence(process.pvMonitor)
process.dqmoffline_step = cms.EndPath(process.DQMOfflineVertex)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

process.vertexing_step = cms.Path(process.offlinePrimaryVertices4D)
process.vertexing_step_withPID = cms.Path(process.offlinePrimaryVertices4DwithPID)
process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(process.vertexing_step,process.vertexing_step_withPID,process.prevalidation_step,process.dqmoffline_step,process.DQMoutput_step,process.output_step)

