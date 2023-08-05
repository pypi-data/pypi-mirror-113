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


"""Provide a ChemAxon-based factory for molecular entities."""


from typing import Optional

from ..cheminfo import AbstractMolecularEntityFactory, Microspecies, MolecularEntity
from .chemaxon_error import ChemAxonError
from .chemaxon_major_microspecies_service import ChemAxonMajorMicrospeciesService
from .chemaxon_molecule import ChemAxonMolecule
from .chemaxon_proton_dissociation_constants_service import (
    ChemAxonProtonDissociationConstantsService,
)


class ChemAxonMolecularEntityFactory(AbstractMolecularEntityFactory):
    """Define a factory for molecular entities that uses ChemAxon services."""

    @classmethod
    def build_with_services(
        cls,
        molecule: ChemAxonMolecule,
        majorms_service: ChemAxonMajorMicrospeciesService,
        pka_service: ChemAxonProtonDissociationConstantsService,
        inchikey: Optional[str] = None,
        inchi: Optional[str] = None,
        smiles: Optional[str] = None,
    ) -> MolecularEntity:
        """Return a molecular entity built from ChemAxon services."""
        errors = []
        if inchikey is None:
            try:
                inchikey = molecule.to_inchikey()
            except ChemAxonError as exc:
                exc.errors.append("The InChIKey is a required attribute.")
                raise ChemAxonError(errors=exc.errors, warnings=exc.warnings) from exc
        if inchi is None:
            try:
                inchi = molecule.to_inchi()
            except ChemAxonError as exc:
                exc.errors.append("The InChI is a required attribute.")
                raise ChemAxonError(errors=exc.errors, warnings=exc.warnings) from exc
        if smiles is None:
            try:
                smiles = molecule.to_smiles()
            except ChemAxonError as exc:
                errors.extend(cls._create_error_messages(exc))
        result = MolecularEntity(inchikey=inchikey, inchi=inchi, smiles=smiles)
        try:
            result.pka_values = pka_service.estimate_pka_values(molecule)
        except ChemAxonError as exc:
            errors.extend(cls._create_error_messages(exc))
        try:
            result.microspecies = [
                Microspecies(
                    is_major=True,
                    smiles=majorms_service.estimate_major_microspecies(
                        molecule
                    ).to_smiles(),
                )
            ]
        except ChemAxonError as exc:
            errors.extend(cls._create_error_messages(exc))
        result.errors = errors
        return result
