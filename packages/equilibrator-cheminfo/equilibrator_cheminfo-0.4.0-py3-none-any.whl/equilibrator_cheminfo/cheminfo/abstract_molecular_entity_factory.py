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


"""Provide an abstract factory class interface for building molecular entities."""

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from ..error import EquilibratorCheminformaticsError
from .abstract_major_microspecies_service import AbstractMajorMicrospeciesService
from .abstract_molecule import AbstractMolecule
from .abstract_proton_dissociation_constants_service import (
    AbstractProtonDissociationConstantsService,
)
from .error_message import ErrorMessage, SeverityLevel
from .microspecies import Microspecies
from .molecular_entity import MolecularEntity


class AbstractMolecularEntityFactory(ABC):
    """Define an abstract factory class interface for building molecular entities."""

    @classmethod
    @abstractmethod
    def build_with_services(
        cls,
        molecule: AbstractMolecule,
        majorms_service: AbstractMajorMicrospeciesService,
        pka_service: AbstractProtonDissociationConstantsService,
    ) -> MolecularEntity:
        """Return a molecular entity built from services."""
        raise NotImplementedError()

    @classmethod
    def build(
        cls,
        inchikey: str,
        inchi: str,
        smiles: Optional[str] = None,
        microspecies: Iterable[Microspecies] = (),
        pka_values: Iterable[float] = (),
        errors: Iterable[ErrorMessage] = (),
    ) -> MolecularEntity:
        """Return a molecular entity built from the provided values."""
        result = MolecularEntity(inchikey=inchikey, inchi=inchi, smiles=smiles)
        result.microspecies = list(microspecies)
        result.pka_values = list(pka_values)
        result.errors = list(errors)
        return result

    @classmethod
    def build_from_error(
        cls,
        inchikey: str,
        inchi: str,
        error: EquilibratorCheminformaticsError,
        smiles: Optional[str] = None,
    ) -> MolecularEntity:
        """Return a slim molecular entity mostly built from an exception."""
        result = MolecularEntity(inchikey=inchikey, inchi=inchi, smiles=smiles)
        result.errors = cls._create_error_messages(error)
        return result

    @classmethod
    def _create_error_messages(
        cls,
        error: EquilibratorCheminformaticsError,
    ) -> List[ErrorMessage]:
        """Return a list of error messages from an exception instance."""
        result = [
            ErrorMessage(message=msg, level=SeverityLevel.ERROR) for msg in error.errors
        ]
        result.extend(
            (
                ErrorMessage(message=msg, level=SeverityLevel.WARNING)
                for msg in error.warnings
            )
        )
        return result
