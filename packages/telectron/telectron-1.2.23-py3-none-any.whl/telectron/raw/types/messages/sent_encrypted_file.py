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


class SentEncryptedFile(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.messages.SentEncryptedMessage`.

    Details:
        - Layer: ``129``
        - ID: ``0x9493ff32``

    Parameters:
        date: ``int`` ``32-bit``
        file: :obj:`EncryptedFile <telectron.raw.base.EncryptedFile>`

    See Also:
        This object can be returned by 3 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.SendEncrypted <telectron.raw.functions.messages.SendEncrypted>`
            - :obj:`messages.SendEncryptedFile <telectron.raw.functions.messages.SendEncryptedFile>`
            - :obj:`messages.SendEncryptedService <telectron.raw.functions.messages.SendEncryptedService>`
    """

    __slots__: List[str] = ["date", "file"]

    ID = 0x9493ff32
    QUALNAME = "types.messages.SentEncryptedFile"

    def __init__(self, *, date: int, file: "raw.base.EncryptedFile") -> None:
        self.date = date  # int
        self.file = file  # EncryptedFile

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SentEncryptedFile":
        # No flags
        
        date = Int.read(data)
        
        file = TLObject.read(data)
        
        return SentEncryptedFile(date=date, file=file)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(Int(self.date))
        
        data.write(self.file.write())
        
        return data.getvalue()
