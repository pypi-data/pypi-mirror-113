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


class ExportedChatInviteReplaced(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.messages.ExportedChatInvite`.

    Details:
        - Layer: ``129``
        - ID: ``0x222600ef``

    Parameters:
        invite: :obj:`ExportedChatInvite <telectron.raw.base.ExportedChatInvite>`
        new_invite: :obj:`ExportedChatInvite <telectron.raw.base.ExportedChatInvite>`
        users: List of :obj:`User <telectron.raw.base.User>`

    See Also:
        This object can be returned by 2 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetExportedChatInvite <telectron.raw.functions.messages.GetExportedChatInvite>`
            - :obj:`messages.EditExportedChatInvite <telectron.raw.functions.messages.EditExportedChatInvite>`
    """

    __slots__: List[str] = ["invite", "new_invite", "users"]

    ID = 0x222600ef
    QUALNAME = "types.messages.ExportedChatInviteReplaced"

    def __init__(self, *, invite: "raw.base.ExportedChatInvite", new_invite: "raw.base.ExportedChatInvite", users: List["raw.base.User"]) -> None:
        self.invite = invite  # ExportedChatInvite
        self.new_invite = new_invite  # ExportedChatInvite
        self.users = users  # Vector<User>

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ExportedChatInviteReplaced":
        # No flags
        
        invite = TLObject.read(data)
        
        new_invite = TLObject.read(data)
        
        users = TLObject.read(data)
        
        return ExportedChatInviteReplaced(invite=invite, new_invite=new_invite, users=users)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.invite.write())
        
        data.write(self.new_invite.write())
        
        data.write(Vector(self.users))
        
        return data.getvalue()
