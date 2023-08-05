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


"""Provide a molecular entity repository backed by an ORM."""


from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from ..cheminfo import (
    AbstractMolecularEntityRepository,
    ErrorMessage,
    Microspecies,
    MolecularEntity,
)
from ..error import EquilibratorCheminformaticsError
from ..inchi_helpers import drop_protonation
from . import ORMMicrospecies
from .orm_base import Session
from .orm_error_message import ORMErrorMessage
from .orm_molecular_entity import ORMMolecularEntity
from .orm_proton_dissociation_constant import ORMProtonDissociationConstant


class ORMMolecularEntityRepository(AbstractMolecularEntityRepository):
    """Define an ORM-based molecular entity repository."""

    def __init__(self, *, session: Session, **kwargs) -> None:
        """Initialize the base."""
        super().__init__(**kwargs)
        self._session = session

    @classmethod
    def build_from_orm(cls, molecular_entity: ORMMolecularEntity) -> MolecularEntity:
        """Build an ORM representation of a molecular entity."""
        result = MolecularEntity(
            inchikey=molecular_entity.inchikey,
            inchi=molecular_entity.inchi,
            smiles=molecular_entity.smiles,
        )
        result.microspecies = [
            Microspecies(is_major=ms.is_major, smiles=ms.smiles)
            for ms in molecular_entity.microspecies
        ]
        result.pka_values = [
            pka.value for pka in molecular_entity.proton_dissociation_constants
        ]
        result.errors = [
            ErrorMessage(message=error.message, level=error.level)
            for error in molecular_entity.error_messages
        ]
        return result

    def find_by_inchikey(self, inchikey: str) -> MolecularEntity:
        """Find a molecular entity in the repository by its InChIKey."""
        try:
            entity: ORMMolecularEntity = (
                self._session.query(ORMMolecularEntity)
                .options(
                    selectinload(ORMMolecularEntity.proton_dissociation_constants)
                    .selectinload(ORMMolecularEntity.microspecies)
                    .selectinload(ORMMolecularEntity.error_messages)
                )
                .filter_by(inchikey=drop_protonation(inchikey))
                .one()
            )
        except NoResultFound:
            raise EquilibratorCheminformaticsError(
                errors=[f"{drop_protonation(inchikey)} is not in the repository."]
            )
        return self.build_from_orm(entity)

    def update(self, molecular_entity: MolecularEntity) -> None:
        """Update a molecular entity in the repository."""
        try:
            result: ORMMolecularEntity = (
                self._session.query(ORMMolecularEntity)
                .options(selectinload(ORMMolecularEntity.proton_dissociation_constants))
                .options(selectinload(ORMMolecularEntity.microspecies))
                .options(selectinload(ORMMolecularEntity.error_messages))
                .filter_by(inchikey=drop_protonation(molecular_entity.inchikey))
                .one()
            )
        except NoResultFound:
            raise EquilibratorCheminformaticsError(
                errors=[f"{molecular_entity.inchikey} is not in the repository."]
            )
        result.microspecies = [
            ORMMicrospecies(is_major=ms.is_major, smiles=ms.smiles)
            for ms in molecular_entity.microspecies
        ]
        result.proton_dissociation_constants = [
            ORMProtonDissociationConstant(value=pka)
            for pka in molecular_entity.pka_values
        ]
        result.error_messages = [
            ORMErrorMessage(message=error.message, level=error.level)
            for error in molecular_entity.errors
        ]
        self._session.add(result)
        self._session.commit()

    def add(self, molecular_entity: MolecularEntity) -> None:
        """Add a molecular entity to the repository."""
        result = ORMMolecularEntity(
            inchikey=molecular_entity.inchikey,
            inchi=molecular_entity.inchi,
            smiles=molecular_entity.smiles,
        )
        result.microspecies = [
            ORMMicrospecies(is_major=ms.is_major, smiles=ms.smiles)
            for ms in molecular_entity.microspecies
        ]
        result.proton_dissociation_constants = [
            ORMProtonDissociationConstant(value=pka)
            for pka in molecular_entity.pka_values
        ]
        result.error_messages = [
            ORMErrorMessage(message=error.message, level=error.level)
            for error in molecular_entity.errors
        ]
        self._session.add(result)
        self._session.commit()
