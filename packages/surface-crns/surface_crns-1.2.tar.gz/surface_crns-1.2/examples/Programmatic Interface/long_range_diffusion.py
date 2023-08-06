from surface_crns import SurfaceCRNQueueSimulator
from surface_crns.models.grids import SquareGridWithCornerLeak
import surface_crns.readers as readers

def main():
    manifest_file = "long_range_diffusion.txt"
    manifest_options = \
                readers.manifest_readers.read_manifest(manifest_file)
    init_state = manifest_options["init_state"]

    lattice = SquareGridWithCornerLeak(init_state.shape[0], init_state.shape[1],
                                       0.25)
    lattice.set_global_state(init_state)
    SurfaceCRNQueueSimulator.simulate_surface_crn(manifest_file,
                            init_state = lattice)

if __name__ == "__main__":
    main()