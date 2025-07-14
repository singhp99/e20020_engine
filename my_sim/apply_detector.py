from attpc_engine.detector import (
    DetectorParams,
    ElectronicsParams,
    PadParams,
    Config,
    run_simulation,
    SpyralWriter,
)

from attpc_engine import nuclear_map
from spyral_utils.nuclear.target import load_target, GasTarget
from pathlib import Path

input_path = Path("./output/kinematics/o16a4a_700Torr_161.6MeV_gs.h5")
output_path = Path("/Users/mahesh/Desktop/academics/spyral_eng/my_sim/output/kinematics/detector")


target_path = Path("/Users/mahesh/Desktop/academics/spyral_eng/my_sim/target.json")

gas = load_target(target_path, nuclear_map)
# Check that our target loaded...
if not isinstance(gas, GasTarget):
    raise Exception(f"Could not load target data from {target_path}!")

detector = DetectorParams(
    length=1.0,
    efield=57260.0, #57260.0 is the calculated efield 
    bfield=3.0,
    mpgd_gain=175000,
    gas_target=gas,
    diffusion=0.070, #changed this from 0.077
    fano_factor=0.2,
    w_value=34.0,
)

electronics = ElectronicsParams(
    clock_freq=3.125, #should be half
    amp_gain=900,
    shaping_time=1000,
    micromegas_edge= 91.98, #91.98
    windows_edge= 469.21, #469.21
    adc_threshold=10,
)

pads = PadParams()

config = Config(detector, electronics, pads)
writer = SpyralWriter(output_path, config, 5_000)

def main():
    run_simulation(
        config,
        input_path,
        writer,
    )

if __name__ == "__main__":
    main()