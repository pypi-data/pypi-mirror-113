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


"""Provide a molecular entity."""


from typing import List, Optional

from ..inchi_helpers import drop_proton_layer, drop_protonation
from .error_message import ErrorMessage
from .microspecies import Microspecies


class MolecularEntity:
    """
    Define the molecular entity.

    A molecular entity is according to [1]_,

        Any constitutionally or isotopically distinct atom, molecule, ion, ion
        pair , radical, radical ion , complex, conformer etc., identifiable as a
        separately distinguishable entity. Molecular entity is used in this
        Compendium as a general term for singular entities, irrespective of
        their nature, while chemical species stands for sets or ensembles of
        molecular entities. Note that the name of a compound may refer to the
        respective molecular entity or to the chemical species, e.g. methane,
        may mean a single molecule of CH4 (molecular entity) or a molar amount,
        specified or not (chemical species), participating in a reaction. The
        degree of precision necessary to describe a molecular entity depends on
        the context. For example 'hydrogen molecule' is an adequate definition
        of a certain molecular entity for some purposes, whereas for others it
        is necessary to distinguish the electronic state and/or vibrational
        state and/or nuclear spin, etc. of the hydrogen molecule.

    References
    ----------
    .. [1] PAC, 1994, 66, 1077. (Glossary of terms used in physical organic
        chemistry (IUPAC Recommendations 1994)) on page 1142
        https://goldbook.iupac.org/terms/view/M03986

    """

    def __init__(
        self, *, inchikey: str, inchi: str, smiles: Optional[str] = None, **kwargs
    ) -> None:
        """Initialize the base."""
        super().__init__(**kwargs)
        self._inchikey = None
        self._inchi = None
        self.smiles = smiles
        self.microspecies: List[Microspecies] = []
        self.pka_values: List[float] = []
        self.errors: List[ErrorMessage] = []
        self.inchikey = inchikey
        self.inchi = inchi

    @property
    def inchikey(self) -> str:
        """Return the InChIKey."""
        return self._inchikey

    @inchikey.setter
    def inchikey(self, inchikey: str) -> None:
        """Set the InChIKey dropping the protonation state if any exists."""
        self._inchikey = drop_protonation(inchikey)

    @property
    def inchi(self) -> str:
        """Return the InChI."""
        return self._inchi

    @inchi.setter
    def inchi(self, inchi: str) -> None:
        """Set the InChI dropping the proton layer if any exists."""
        self._inchi = drop_proton_layer(inchi)
