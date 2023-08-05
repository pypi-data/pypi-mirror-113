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


class LoginTokenSuccess(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.auth.LoginToken`.

    Details:
        - Layer: ``129``
        - ID: ``0x390d5c5e``

    Parameters:
        authorization: :obj:`auth.Authorization <telectron.raw.base.auth.Authorization>`

    See Also:
        This object can be returned by 2 methods:

        .. hlist::
            :columns: 2

            - :obj:`auth.ExportLoginToken <telectron.raw.functions.auth.ExportLoginToken>`
            - :obj:`auth.ImportLoginToken <telectron.raw.functions.auth.ImportLoginToken>`
    """

    __slots__: List[str] = ["authorization"]

    ID = 0x390d5c5e
    QUALNAME = "types.auth.LoginTokenSuccess"

    def __init__(self, *, authorization: "raw.base.auth.Authorization") -> None:
        self.authorization = authorization  # auth.Authorization

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "LoginTokenSuccess":
        # No flags
        
        authorization = TLObject.read(data)
        
        return LoginTokenSuccess(authorization=authorization)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.authorization.write())
        
        return data.getvalue()
