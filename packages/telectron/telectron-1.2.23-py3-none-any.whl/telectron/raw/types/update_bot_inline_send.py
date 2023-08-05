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


class UpdateBotInlineSend(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.Update`.

    Details:
        - Layer: ``129``
        - ID: ``0xe48f964``

    Parameters:
        user_id: ``int`` ``32-bit``
        query: ``str``
        id: ``str``
        geo (optional): :obj:`GeoPoint <telectron.raw.base.GeoPoint>`
        msg_id (optional): :obj:`InputBotInlineMessageID <telectron.raw.base.InputBotInlineMessageID>`
    """

    __slots__: List[str] = ["user_id", "query", "id", "geo", "msg_id"]

    ID = 0xe48f964
    QUALNAME = "types.UpdateBotInlineSend"

    def __init__(self, *, user_id: int, query: str, id: str, geo: "raw.base.GeoPoint" = None, msg_id: "raw.base.InputBotInlineMessageID" = None) -> None:
        self.user_id = user_id  # int
        self.query = query  # string
        self.id = id  # string
        self.geo = geo  # flags.0?GeoPoint
        self.msg_id = msg_id  # flags.1?InputBotInlineMessageID

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "UpdateBotInlineSend":
        flags = Int.read(data)
        
        user_id = Int.read(data)
        
        query = String.read(data)
        
        geo = TLObject.read(data) if flags & (1 << 0) else None
        
        id = String.read(data)
        
        msg_id = TLObject.read(data) if flags & (1 << 1) else None
        
        return UpdateBotInlineSend(user_id=user_id, query=query, id=id, geo=geo, msg_id=msg_id)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.geo is not None else 0
        flags |= (1 << 1) if self.msg_id is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.user_id))
        
        data.write(String(self.query))
        
        if self.geo is not None:
            data.write(self.geo.write())
        
        data.write(String(self.id))
        
        if self.msg_id is not None:
            data.write(self.msg_id.write())
        
        return data.getvalue()
