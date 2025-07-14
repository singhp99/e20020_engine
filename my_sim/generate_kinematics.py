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
from spyral_utils.nuclear.target import load_target, GasTarget
from pathlib import Path
import numpy as np

output_path = Path("./output/kinematics/o16a4a_700Torr_161.6MeV_gs.h5")
target_path = Path("./target.json")

target = load_target(target_path, nuclear_map)
# Check that our target loaded...
if not isinstance(target, GasTarget):
    raise Exception(f"Could not load target data from {target_path}!")

nevents = 30000

beam_energy = 161.6 # MeV

pipeline = KinematicsPipeline(
    [
        Reaction(
            target=nuclear_map.get_data(2, 4), # alpha
            projectile=nuclear_map.get_data(8, 16), # 16O
            ejectile=nuclear_map.get_data(2, 4), # alpha
        ),
        # Decay(
        #     parent=nuclear_map.get_data(8,16), #16O
        #     residual_1=nuclear_map.get_data(2,4),
        # ),
        # Decay(
        #     parent=nuclear_map.get_data(6,12), #12C
        #     residual_1=nuclear_map.get_data(2,4),
        # ),
        # Decay(
        #     parent=nuclear_map.get_data(4,8), #8Be
        #     residual_1=nuclear_map.get_data(2,4),
        # ),
        # Decay(
        #     parent=nuclear_map.get_data(2,4), #4He
        #     residual_1=nuclear_map.get_data(2,4),
        # ),

    ], 

    # [ExcitationGaussian(15.097, 0.001),ExcitationGaussian(7.654, 0.001),ExcitationGaussian(0, 0.001),ExcitationGaussian(0.0, 0.001)], # No width to ground state #need to add energues above threhold  make the width super narrow
    [ExcitationGaussian(0, 0.001)],

    # [PolarUniform(0.0, np.pi),PolarUniform(0.0, np.pi),PolarUniform(0.0, np.pi),PolarUniform(0.0, np.pi)], # Full angular range 0 deg to 180 deg
    [PolarUniform(0.0, np.pi)],
    
    beam_energy=161.6, # MeV
    target_material=KinematicsTargetMaterial(
        material=target, z_range=(0.0, 1.0), rho_sigma=0.007
    ),
)

def main():
    run_kinematics_pipeline(pipeline, nevents, output_path)

if __name__ == "__main__":
    main()





        #     Decay(
        #     parent=nuclear_map.get_data(6,12),
        #     residual_1=nuclear_map.get_data(2,4),
        # ),
        # Decay(
        #     parent=nuclear_map.get_data(4,8),
        #     residual_1=nuclear_map.get_data(2,4),
        # ),
        # Decay(
        #     parent=nuclear_map.get_data(2,4),
        #     residual_1=nuclear_map.get_data(2,4),
        # # ),

        # ,ExcitationGaussian(7.654, 0.001),ExcitationGaussian(0, 0.001),ExcitationGaussian(0.0, 0.001),

        #PolarUniform(0.0, np.pi),PolarUniform(0.0, np.pi),PolarUniform(0.0, np.pi,)