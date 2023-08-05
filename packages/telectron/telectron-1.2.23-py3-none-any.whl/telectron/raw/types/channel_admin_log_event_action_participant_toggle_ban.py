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


class ChannelAdminLogEventActionParticipantToggleBan(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``129``
        - ID: ``0xe6d83d7e``

    Parameters:
        prev_participant: :obj:`ChannelParticipant <telectron.raw.base.ChannelParticipant>`
        new_participant: :obj:`ChannelParticipant <telectron.raw.base.ChannelParticipant>`
    """

    __slots__: List[str] = ["prev_participant", "new_participant"]

    ID = 0xe6d83d7e
    QUALNAME = "types.ChannelAdminLogEventActionParticipantToggleBan"

    def __init__(self, *, prev_participant: "raw.base.ChannelParticipant", new_participant: "raw.base.ChannelParticipant") -> None:
        self.prev_participant = prev_participant  # ChannelParticipant
        self.new_participant = new_participant  # ChannelParticipant

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ChannelAdminLogEventActionParticipantToggleBan":
        # No flags
        
        prev_participant = TLObject.read(data)
        
        new_participant = TLObject.read(data)
        
        return ChannelAdminLogEventActionParticipantToggleBan(prev_participant=prev_participant, new_participant=new_participant)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.prev_participant.write())
        
        data.write(self.new_participant.write())
        
        return data.getvalue()
