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

output_path = Path("./output/kinematics/mg24_60Torr_161.6MeV_15MeV.h5")
target_path = Path("./target_24Mg.json")

target = load_target(target_path, nuclear_map)
print(type(target))
# Check that our target loaded...
if not isinstance(target, GasMixtureTarget):
    raise Exception(f"Could not load target data from {target_path}!")

nevents = 10000

beam_energy = 60 # MeV

pipeline = KinematicsPipeline(
    [
        Reaction(
            target=nuclear_map.get_data(6, 12), # 12C
            projectile=nuclear_map.get_data(6, 12), # 24Mg
            ejectile=nuclear_map.get_data(2, 4), # alpha
        ),
    ], #add a 20Ne -> p decay now 

    [ExcitationGaussian(20, 0.001)], # No width to ground state #need to add energues above threhold  make the width super narrow
    #[ExcitationGaussian(0, 0.001)],

    [PolarUniform(0.0, np.pi)], # Full angular range 0 deg to 180 deg
    #[PolarUniform(0.0, np.pi)],
    
    beam_energy=60, # MeV
    target_material=KinematicsTargetMaterial(
        material=target, z_range=(0.0, 1.0), rho_sigma=0.007
    ),
)

def main():
    run_kinematics_pipeline(pipeline, nevents, output_path)

if __name__ == "__main__":
    main()