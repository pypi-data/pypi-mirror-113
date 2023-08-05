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


class ValidateRequestedInfo(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``129``
        - ID: ``0xdb103170``

    Parameters:
        peer: :obj:`InputPeer <telectron.raw.base.InputPeer>`
        msg_id: ``int`` ``32-bit``
        info: :obj:`PaymentRequestedInfo <telectron.raw.base.PaymentRequestedInfo>`
        save (optional): ``bool``

    Returns:
        :obj:`payments.ValidatedRequestedInfo <telectron.raw.base.payments.ValidatedRequestedInfo>`
    """

    __slots__: List[str] = ["peer", "msg_id", "info", "save"]

    ID = 0xdb103170
    QUALNAME = "functions.payments.ValidateRequestedInfo"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, info: "raw.base.PaymentRequestedInfo", save: Union[None, bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.info = info  # PaymentRequestedInfo
        self.save = save  # flags.0?true

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ValidateRequestedInfo":
        flags = Int.read(data)
        
        save = True if flags & (1 << 0) else False
        peer = TLObject.read(data)
        
        msg_id = Int.read(data)
        
        info = TLObject.read(data)
        
        return ValidateRequestedInfo(peer=peer, msg_id=msg_id, info=info, save=save)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.save else 0
        data.write(Int(flags))
        
        data.write(self.peer.write())
        
        data.write(Int(self.msg_id))
        
        data.write(self.info.write())
        
        return data.getvalue()
