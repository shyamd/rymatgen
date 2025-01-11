import time
import argparse
from pymatgen.core import Molecule, Structure, Lattice


def benchmark_molecule_creation(iterations: int, scale: int):
    """Benchmark molecule creation for pymatgen."""
    molecule_data = {
        "species": ["H", "H", "O"] * scale,
        "coords": [[0, 0, 0], [0, 0, 1], [0, 1, 0]] * scale,
    }

    # Create Molecule
    start_time = time.time()
    for _ in range(iterations):
        molecule = Molecule(molecule_data["species"], molecule_data["coords"])
    creation_time = time.time() - start_time

    num_atoms = len(molecule_data["species"])
    print(
        f"Pymatgen Molecule Creation ({num_atoms} atoms {iterations} iterations): {creation_time / iterations:.6f} seconds/iteration"
    )

    # Serialize Molecule
    start_time = time.time()
    for _ in range(iterations):
        mol_json = molecule.as_dict()
    serialization_time = time.time() - start_time
    print(
        f"Pymatgen Molecule Serialization ({num_atoms} atoms {iterations} iterations): {serialization_time / iterations:.6f} seconds/iteration"
    )

    # Deserialize Molecule
    start_time = time.time()
    for _ in range(iterations):
        pymatgen_molecule = Molecule.from_dict(mol_json)
    deserialization_time = time.time() - start_time
    print(
        f"Pymatgen Molecule Deserialization ({num_atoms} atoms {iterations} iterations): {deserialization_time / iterations:.6f} seconds/iteration"
    )


def benchmark_crystal_structure_creation(iterations: int, scale: int):
    """Benchmark crystal structure creation for pymatgen."""
    lattice = Lattice(matrix=[[5.64, 0, 0], [0, 5.64, 0], [0, 0, 5.64 * scale]])
    species = ["Na"] * scale + ["Cl"] * scale
    coords = [[0, 0, i / scale] for i in range(scale)] + [
        [0, 0, (i + 0.5) / scale] for i in range(scale)
    ]

    # Benchmark Pymatgen Structure
    start_time = time.time()
    for _ in range(iterations):
        structure = Structure(lattice, species, coords)
    creation_time = time.time() - start_time

    num_atoms = len(species)
    print(
        f"Pymatgen Structure Creation ({num_atoms} atoms {iterations} iterations): {creation_time / iterations:.6f} seconds/iteration"
    )

    # Serialize Structure
    start_time = time.time()
    for _ in range(iterations):
        struct_json = structure.as_dict()
    serialization_time = time.time() - start_time
    print(
        f"Pymatgen Structure Serialization ({iterations} iterations): {serialization_time/iterations:.6f} seconds/iterations"
    )

    # Deserialize Structure
    start_time = time.time()
    for _ in range(iterations):
        pymatgen_structure = Structure.from_dict(struct_json)
    deserialization_time = time.time() - start_time
    print(
        f"Pymatgen Structure Deserialization ({iterations} iterations): {deserialization_time/iterations:.6f} seconds/iterations"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark materials informatics data structures."
    )
    parser.add_argument(
        "-n",
        "--iterations",
        type=int,
        default=1000,
        help="Number of iterations for the benchmark (default: 1000)",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=50,
        help="Scaling factor for molecule and materials (default: 50)",
    )
    args = parser.parse_args()

    print("Starting Benchmarks...\n")
    benchmark_molecule_creation(args.iterations, args.scale)
    print()
    benchmark_crystal_structure_creation(args.iterations, args.scale)
    print()
