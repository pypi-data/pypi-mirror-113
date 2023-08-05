#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SecureValueErrorReverseSide(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.SecureValueError`.

    Details:
        - Layer: ``129``
        - ID: ``0x868a2aa5``

    Parameters:
        type: :obj:`SecureValueType <telectron.raw.base.SecureValueType>`
        file_hash: ``bytes``
        text: ``str``
    """

    __slots__: List[str] = ["type", "file_hash", "text"]

    ID = 0x868a2aa5
    QUALNAME = "types.SecureValueErrorReverseSide"

    def __init__(self, *, type: "raw.base.SecureValueType", file_hash: bytes, text: str) -> None:
        self.type = type  # SecureValueType
        self.file_hash = file_hash  # bytes
        self.text = text  # string

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SecureValueErrorReverseSide":
        # No flags
        
        type = TLObject.read(data)
        
        file_hash = Bytes.read(data)
        
        text = String.read(data)
        
        return SecureValueErrorReverseSide(type=type, file_hash=file_hash, text=text)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.type.write())
        
        data.write(Bytes(self.file_hash))
        
        data.write(String(self.text))
        
        return data.getvalue()
