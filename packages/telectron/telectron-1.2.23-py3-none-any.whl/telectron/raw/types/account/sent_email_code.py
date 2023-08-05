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


class SentEmailCode(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.account.SentEmailCode`.

    Details:
        - Layer: ``129``
        - ID: ``0x811f854f``

    Parameters:
        email_pattern: ``str``
        length: ``int`` ``32-bit``

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`account.SendVerifyEmailCode <telectron.raw.functions.account.SendVerifyEmailCode>`
    """

    __slots__: List[str] = ["email_pattern", "length"]

    ID = 0x811f854f
    QUALNAME = "types.account.SentEmailCode"

    def __init__(self, *, email_pattern: str, length: int) -> None:
        self.email_pattern = email_pattern  # string
        self.length = length  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SentEmailCode":
        # No flags
        
        email_pattern = String.read(data)
        
        length = Int.read(data)
        
        return SentEmailCode(email_pattern=email_pattern, length=length)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(String(self.email_pattern))
        
        data.write(Int(self.length))
        
        return data.getvalue()
