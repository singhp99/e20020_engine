from attpc_engine.kinematics import (
    KinematicsPipeline,
    KinematicsTargetMaterial,
    ExcitationGaussian,
    PolarUniform,
    run_kinematics_pipeline,
    Reaction,
    Decay,
)
from attpc_engine import nuclear_map
from spyral_utils.nuclear.target import load_target, GasTarget,GasMixtureTarget
from pathlib import Path
import numpy as np

output_path = Path("/Users/pranjalsingh/Desktop/research_space_engine/e20020_engine/my_sim/output/kinematics/mg24_60Torr_60MeV_123.h5")
target_path = Path("/Users/pranjalsingh/Desktop/research_space_engine/e20020_engine/my_sim/target_24Mg.json")

target = load_target(target_path, nuclear_map)
print(type(target))
# Check that our target loaded...
if not isinstance(target, GasMixtureTarget):
    raise Exception(f"Could not load target data from {target_path}!")

nevents = 80000

beam_energy = 80 # MeV

pipeline = KinematicsPipeline(
    [
        Reaction(
            target=nuclear_map.get_data(6, 12), # 12C
            projectile=nuclear_map.get_data(6, 12), # 12C
            ejectile=nuclear_map.get_data(2, 4), # alpha
        ),
        Decay(
            parent=nuclear_map.get_data(10,20), #20Ne
            residual_1=nuclear_map.get_data(1,1),
        ),
    ], #add a 20Ne -> p decay now 

    [ExcitationGaussian(40, 0.001), ExcitationGaussian(25, 0.001)], # No width to ground state #need to add energies above threshold  make the width super narrow
    #[ExcitationGaussian(0, 0.001)],

    [PolarUniform(0.0, np.pi), PolarUniform(0.0, np.pi)], # Full angular range 0 deg to 180 deg
    #[PolarUniform(0.0, np.pi)],
    
    beam_energy=80, # MeV
    target_material=KinematicsTargetMaterial(
        material=target, z_range=(0.0, 1.0), rho_sigma=0.007
    ),
)

def main():
    run_kinematics_pipeline(pipeline, nevents, output_path)

if __name__ == "__main__":
    main()