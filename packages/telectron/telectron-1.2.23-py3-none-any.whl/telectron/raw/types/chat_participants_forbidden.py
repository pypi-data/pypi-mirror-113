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


class ChatParticipantsForbidden(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.ChatParticipants`.

    Details:
        - Layer: ``129``
        - ID: ``0xfc900c2b``

    Parameters:
        chat_id: ``int`` ``32-bit``
        self_participant (optional): :obj:`ChatParticipant <telectron.raw.base.ChatParticipant>`
    """

    __slots__: List[str] = ["chat_id", "self_participant"]

    ID = 0xfc900c2b
    QUALNAME = "types.ChatParticipantsForbidden"

    def __init__(self, *, chat_id: int, self_participant: "raw.base.ChatParticipant" = None) -> None:
        self.chat_id = chat_id  # int
        self.self_participant = self_participant  # flags.0?ChatParticipant

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ChatParticipantsForbidden":
        flags = Int.read(data)
        
        chat_id = Int.read(data)
        
        self_participant = TLObject.read(data) if flags & (1 << 0) else None
        
        return ChatParticipantsForbidden(chat_id=chat_id, self_participant=self_participant)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.self_participant is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.chat_id))
        
        if self.self_participant is not None:
            data.write(self.self_participant.write())
        
        return data.getvalue()
