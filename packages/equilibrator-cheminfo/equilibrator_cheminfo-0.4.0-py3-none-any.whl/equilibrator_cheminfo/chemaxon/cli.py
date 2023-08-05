#!/usr/bin/env python3


# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide commands for the ChemAxon Marvin pipeline."""


import argparse
import logging
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Optional, TypedDict

import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm

from .. import orm
from ..cheminfo import MolecularEntity
from ..inchi_helpers import drop_column_proton_layer, drop_column_protonation
from .chemaxon_error import ChemAxonError
from .chemaxon_major_microspecies_service import ChemAxonMajorMicrospeciesService
from .chemaxon_molecular_entity_factory import ChemAxonMolecularEntityFactory
from .chemaxon_molecule import ChemAxonMolecule
from .chemaxon_proton_dissociation_constants_service import (
    ChemAxonProtonDissociationConstantsService,
)


logger = logging.getLogger()


class MolecularEntityMap(TypedDict, total=False):
    """Define an object map for the molecular entity."""

    id: int
    inchikey: str
    inchi: str
    smiles: Optional[str]


def _init_worker(minimum_ph: float, maximum_ph: float, fixed_ph: float) -> None:
    """Initialize a worker with globally configured ChemAxon adapters."""
    global _pka
    global _majorms

    _pka = ChemAxonProtonDissociationConstantsService(
        minimum_ph=minimum_ph,
        minimum_basic_pka=minimum_ph,
        maximum_ph=maximum_ph,
        maximum_acidic_pka=maximum_ph,
    )
    _majorms = ChemAxonMajorMicrospeciesService(ph=fixed_ph)


def create_molecular_entity(molecule: MolecularEntityMap) -> MolecularEntity:
    """Run all ChemAxon Marvin predictions and handle errors as appropriate."""
    global _pka
    global _majorms

    try:
        if pd.notnull(molecule["smiles"]):
            mol = ChemAxonMolecule.from_smiles(molecule["smiles"])
        else:
            mol = ChemAxonMolecule.from_inchi(molecule["inchi"])
    except ChemAxonError as error:
        return ChemAxonMolecularEntityFactory.build_from_error(
            inchikey=molecule["inchikey"],
            inchi=molecule["inchi"],
            error=error,
            smiles=molecule["smiles"],
        )
    else:
        return ChemAxonMolecularEntityFactory.build_with_services(
            molecule=mol,
            majorms_service=_majorms,
            pka_service=_pka,
            inchikey=molecule["inchikey"],
            inchi=molecule["inchi"],
            smiles=molecule["smiles"],
        )


def transform_molecular_entities(
    session: orm.Session,
    molecules: pd.DataFrame,
    minimum_ph: float,
    maximum_ph: float,
    fixed_ph: float,
    processes: int,
    batch_size: int = 10_000,
) -> None:
    """Coordinate predictions on all molecules in parallel and load results."""
    repo = orm.ORMMolecularEntityRepository(session=session)
    args = molecules.to_dict(orient="records")
    chunk_size = min(len(args) // processes, batch_size)
    with multiprocessing.get_context("spawn").Pool(
        processes=processes,
        initializer=_init_worker,
        initargs=(minimum_ph, maximum_ph, fixed_ph),
    ) as pool:
        result_iter = pool.imap_unordered(
            create_molecular_entity,
            args,
            chunksize=chunk_size,
        )
        for mol in tqdm(
            result_iter, total=len(args), desc="Molecular Entity", unit_scale=True
        ):
            repo.add(mol)


def transform_molecular_entities_sequentially(
    session: orm.Session,
    molecules: pd.DataFrame,
    minimum_ph: float,
    maximum_ph: float,
    fixed_ph: float,
) -> None:
    """Coordinate predictions on all molecules sequentially and load results."""
    repo = orm.ORMMolecularEntityRepository(session=session)
    args = molecules.to_dict(orient="records")
    _init_worker(minimum_ph, maximum_ph, fixed_ph)
    for obj in tqdm(args, total=len(args), desc="Molecular Entity", unit_scale=True):
        mol = create_molecular_entity(obj)
        repo.add(mol)


def manage_molecular_entities(
    session: orm.Session,
    molecules: pd.DataFrame,
    minimum_ph: float,
    maximum_ph: float,
    ph: float,
    processes: int,
):
    """Coordinate high-level calls and argument transformation."""
    if processes > 1:
        transform_molecular_entities(
            session,
            molecules,
            minimum_ph,
            maximum_ph,
            ph,
            processes,
        )
    else:
        transform_molecular_entities_sequentially(
            session,
            molecules,
            minimum_ph,
            maximum_ph,
            ph,
        )


def summarize_molecular_entities(session: orm.Session):
    """Summarize the information in the created molecular entity database."""
    logger.info("Molecular entity summary:")
    base_query = session.query(orm.ORMMolecularEntity.id).select_from(
        orm.ORMMolecularEntity
    )
    num_total = base_query.count()
    logger.info(f"- {num_total:n} unique InChIKeys")
    num_with_pka = base_query.join(orm.ORMProtonDissociationConstant).distinct().count()
    logger.info(f"- {num_with_pka:n} ({num_with_pka / num_total:.2%}) with pKa values")
    num_with_major_ms = base_query.join(orm.ORMMicrospecies).distinct().count()
    logger.info(
        f"- {num_with_major_ms:n} ({num_with_major_ms / num_total:.2%}) with major "
        f"microspecies at pH 7"
    )
    num_with_error = base_query.join(orm.ORMErrorMessage).distinct().count()
    logger.info(f"- {num_with_error:n} ({num_with_error / num_total:.2%}) with errors:")
    if num_with_error > 0:
        num_with_error_but_pka = (
            base_query.join(orm.ORMErrorMessage)
            .join(orm.ORMProtonDissociationConstant)
            .distinct()
            .count()
        )
        logger.info(
            f"  - {num_with_error_but_pka:n} "
            f"({num_with_error_but_pka / num_with_error:.2%}) "
            f"of those with pKa values"
        )
        num_with_error_but_major_ms = (
            base_query.join(orm.ORMErrorMessage)
            .join(orm.ORMMicrospecies)
            .distinct()
            .count()
        )
        logger.info(
            f"  - {num_with_error_but_major_ms:n} "
            f"({num_with_error_but_major_ms / num_with_error:.2%}) "
            f"of those with major microspecies at pH 7"
        )


def create_session(db_url: str) -> orm.Session:
    """Create a SQLAlchemy session with an active database connection."""
    return orm.Session(bind=create_engine(db_url))


def transform_molecules(molecules: pd.DataFrame) -> pd.DataFrame:
    """Transform molecules to drop protonation information and return unique ones."""
    logger.debug("Ignore rows with missing InChIs.")
    view = molecules.loc[molecules["inchi"].notnull(), ["inchikey", "inchi", "smiles"]]
    logger.debug("Found %d entries.", len(view))
    logger.debug("Drop protonation information.")
    result = view.copy()
    result["inchikey"] = drop_column_protonation(result["inchikey"])
    result["inchi"] = drop_column_proton_layer(result["inchi"])
    logger.debug("Consider unique InChIKeys only.")
    return result.drop_duplicates(["inchikey", "inchi"])


def manage_molecules(molecules: Path) -> pd.DataFrame:
    """Extract and transform molecules from the given TSV file."""
    logger.info("Extract molecules.")
    raw = pd.read_csv(molecules, sep="\t")
    logger.info(f"Found {len(raw):n} entries.")
    logger.info("Transform molecules.")
    result = transform_molecules(raw)
    logger.info(f"Maintained {len(result):n} entries.")
    assert len(result["inchikey"].unique()) == len(
        result
    ), "InChIKeys are not unique even though they *should* be."
    return result


def orchestrate_etl_molecular_entities(args: argparse.Namespace) -> None:
    """Orchestrate the high-level ETL workflow to for molecular entities."""
    if not args.molecules.is_file():
        raise ValueError(
            f"The TSV file '{args.molecules}' defining the molecules was not found."
        )
    molecules = manage_molecules(args.molecules)
    session = create_session(args.db_url)
    logger.info("Set up clean database.")
    orm.ORMBase.metadata.drop_all(session.bind)
    orm.ORMBase.metadata.create_all(session.bind)
    manage_molecular_entities(
        session, molecules, args.minimum_ph, args.maximum_ph, args.ph, args.processes
    )
    summarize_molecular_entities(session)


def parse_argv() -> argparse.Namespace:
    """Define the command line arguments and immediately parse them."""
    num_processes = len(os.sched_getaffinity(0))
    if not num_processes:
        num_processes = 1
    if num_processes > 1:
        num_processes -= 1

    parser = argparse.ArgumentParser(
        prog="marvin",
        description="Build a molecular entity database containing proton dissociation "
        "constants and major microspecies using ChemAxon Marvin.",
    )
    parser.add_argument(
        "--db-url",
        required=True,
        metavar="URL",
        help="A string interpreted as an rfc1738 compatible database URL.",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        help="The desired log level.",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    parser.add_argument(
        "--minimum-ph",
        type=float,
        default=0.0,
        help="The minimum pH value to consider (default 0).",
    )
    parser.add_argument(
        "--maximum-ph",
        type=float,
        default=14.0,
        help="The maximum pH value to consider (default 14).",
    )
    parser.add_argument(
        "--ph",
        type=float,
        default=7.0,
        help="The pH value at which to determine the major microspecies (default 7).",
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=num_processes,
        help=f"The number of parallel processes to start (default {num_processes}).",
    )
    parser.add_argument(
        "molecules",
        type=Path,
        help="Path to a TSV file with molecules defined by the columns inchikey, "
        "inchi, smiles. Missing values are allowed.",
    )

    return parser.parse_args(sys.argv[1:])


def main() -> None:
    """Coordinate argument parsing and command calling."""
    args = parse_argv()
    logging.basicConfig(level=args.log_level, format="[%(levelname)s] %(message)s")
    orchestrate_etl_molecular_entities(args)
