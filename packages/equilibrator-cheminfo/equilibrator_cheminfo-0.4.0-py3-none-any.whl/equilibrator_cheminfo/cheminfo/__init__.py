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


"""Provide abstract base classes aka interfaces."""


from .abstract_molecule import AbstractMolecule
from .abstract_major_microspecies_service import AbstractMajorMicrospeciesService
from .abstract_proton_dissociation_constants_service import (
    AbstractProtonDissociationConstantsService,
)
from .error_message import ErrorMessage, SeverityLevel
from .microspecies import Microspecies
from .molecular_entity import MolecularEntity
from .abstract_molecular_entity_factory import AbstractMolecularEntityFactory
from .abstract_molecular_entity_repository import AbstractMolecularEntityRepository
