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


class ChannelParticipant(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.channels.ChannelParticipant`.

    Details:
        - Layer: ``129``
        - ID: ``0xdfb80317``

    Parameters:
        participant: :obj:`ChannelParticipant <telectron.raw.base.ChannelParticipant>`
        chats: List of :obj:`Chat <telectron.raw.base.Chat>`
        users: List of :obj:`User <telectron.raw.base.User>`

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`channels.GetParticipant <telectron.raw.functions.channels.GetParticipant>`
    """

    __slots__: List[str] = ["participant", "chats", "users"]

    ID = 0xdfb80317
    QUALNAME = "types.channels.ChannelParticipant"

    def __init__(self, *, participant: "raw.base.ChannelParticipant", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.participant = participant  # ChannelParticipant
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ChannelParticipant":
        # No flags
        
        participant = TLObject.read(data)
        
        chats = TLObject.read(data)
        
        users = TLObject.read(data)
        
        return ChannelParticipant(participant=participant, chats=chats, users=users)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.participant.write())
        
        data.write(Vector(self.chats))
        
        data.write(Vector(self.users))
        
        return data.getvalue()
