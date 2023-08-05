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


class ChannelParticipantsMentions(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.ChannelParticipantsFilter`.

    Details:
        - Layer: ``129``
        - ID: ``0xe04b5ceb``

    Parameters:
        q (optional): ``str``
        top_msg_id (optional): ``int`` ``32-bit``
    """

    __slots__: List[str] = ["q", "top_msg_id"]

    ID = 0xe04b5ceb
    QUALNAME = "types.ChannelParticipantsMentions"

    def __init__(self, *, q: Union[None, str] = None, top_msg_id: Union[None, int] = None) -> None:
        self.q = q  # flags.0?string
        self.top_msg_id = top_msg_id  # flags.1?int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ChannelParticipantsMentions":
        flags = Int.read(data)
        
        q = String.read(data) if flags & (1 << 0) else None
        top_msg_id = Int.read(data) if flags & (1 << 1) else None
        return ChannelParticipantsMentions(q=q, top_msg_id=top_msg_id)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.q is not None else 0
        flags |= (1 << 1) if self.top_msg_id is not None else 0
        data.write(Int(flags))
        
        if self.q is not None:
            data.write(String(self.q))
        
        if self.top_msg_id is not None:
            data.write(Int(self.top_msg_id))
        
        return data.getvalue()
