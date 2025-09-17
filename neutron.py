from LDMX.Framework import ldmxcfg
from LDMX.SimCore import simulator as sim
from LDMX.SimCore import generators as gen
p = ldmxcfg.Process('test')
mySim = sim.simulator( "mySim" )
mySim.setDetector( 'ldmx-det-v14-8gev', True )

p.termLogLevel = 1
myGun = gen.gun('myGun')
myGun.particle = 'neutron' 
myGun.position = [ 0., 0., 0.1 ]  # mm before target, ts3
myGun.direction = [ 0., 0., 1] 
myGun.energy = 0.5 # GeV
mySim.generators.append(myGun)

# mySim.generators = [ gen.single_8gev_e_upstream_tagger() ]
# mySim.beamSpotSmear = [20.,80.,0.]
# mySim.description = 'Basic test Simulation'
p.sequence = [ mySim ]
p.run = 1
p.maxEvents = 100000
p.outputFiles = [ 'neutron_500MeV.root' ]

import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
import LDMX.Hcal.hcal_hardcoded_conditions
import LDMX.Ecal.digi as ecal_digi
import LDMX.Ecal.vetos as ecal_vetos
import LDMX.Hcal.digi as hcal_digi
from LDMX.Hcal import hcal_trig_digi
from LDMX.Ecal import ecal_trig_digi
from LDMX.Trigger import trigger_energy_sums
from LDMX.Trigger import dump_file_writer

p.sequence.extend([
        ecal_digi.EcalDigiProducer(),
        ecal_digi.EcalRecProducer(),
        hcal_digi.HcalDigiProducer(),
        hcal_digi.HcalRecProducer(),
        ])

from LDMX.Recon import pfReco
ecalPF = pfReco.pfEcalClusterProducer()
hcalPF = pfReco.pfHcalClusterProducer()
trackPF = pfReco.pfTrackProducer()
truthPF = pfReco.pfTruthProducer()

# configure clustering options
ecalPF.doSingleCluster = False
hcalPF.clusterHitDist = 100000. # mm
ecalPF.logEnergyWeight = True

hcalPF.doSingleCluster = False
hcalPF.clusterHitDist = 100000. # mm
hcalPF.logEnergyWeight = True

p.sequence.extend([
          ecalPF, hcalPF, trackPF,
          pfReco.pfProducer(),
          truthPF,
])

# p.sequence.append( dump_file_writer.DumpFileWriter() )

# to run over the hcal skim, or other central samples
# if 0:
#     p.sequence = []  # the above is already run
#     p.inputFiles = ['/home/herwig/work/ldmx/local-data/v3.3.6-1e_100PE_241008.root']
#     p.inputFiles = ['/home/herwig/work/ldmx/local-data/v3.3.3_ecalPN_tskim_resim_mc_v14-8gev-8.0GeV-1e-ecal_photonuclear_1020.root']
    
# p.sequence.extend([
#           ecal_trig_digi.EcalTrigPrimDigiProducer(),
#           hcal_trig_digi.HcalTrigPrimDigiProducer(),
#           trigger_energy_sums.EcalTPSelector(),
#           # dump_file_writer.DumpFileWriter(),
#           ])
# p.sequence.extend([
#           trigger_energy_sums.TrigEcalEnergySum(),
#           trigger_energy_sums.TrigEcalClusterProducer(),
#           #trigger_energy_sums.TrigElectronProducer(),
    
#           trigger_energy_sums.TrigHcalEnergySum(),
#           trigger_energy_sums.HcalTPSelector(),
#           trigger_energy_sums.HCalTrigMipReco(),
#      ])

# p.keep = [
#     "drop Trigger.*",
#     "drop Tagger.*",
#     "drop TargetSim.*",
#     "drop HcalSim.*",
#     "drop EcalSim.*",
#     "drop Magnet.*",
#     "drop Recoil.*",
#     "drop Tracker.*",
#     "drop trigScint.*",
#     "drop .*VetoResult.*",
# ]
# # p.keep = [
#  #    "drop EcalVetoResult.*"]
