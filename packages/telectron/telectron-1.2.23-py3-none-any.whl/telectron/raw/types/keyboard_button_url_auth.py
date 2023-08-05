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


class KeyboardButtonUrlAuth(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.KeyboardButton`.

    Details:
        - Layer: ``129``
        - ID: ``0x10b78d29``

    Parameters:
        text: ``str``
        url: ``str``
        button_id: ``int`` ``32-bit``
        fwd_text (optional): ``str``
    """

    __slots__: List[str] = ["text", "url", "button_id", "fwd_text"]

    ID = 0x10b78d29
    QUALNAME = "types.KeyboardButtonUrlAuth"

    def __init__(self, *, text: str, url: str, button_id: int, fwd_text: Union[None, str] = None) -> None:
        self.text = text  # string
        self.url = url  # string
        self.button_id = button_id  # int
        self.fwd_text = fwd_text  # flags.0?string

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "KeyboardButtonUrlAuth":
        flags = Int.read(data)
        
        text = String.read(data)
        
        fwd_text = String.read(data) if flags & (1 << 0) else None
        url = String.read(data)
        
        button_id = Int.read(data)
        
        return KeyboardButtonUrlAuth(text=text, url=url, button_id=button_id, fwd_text=fwd_text)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.fwd_text is not None else 0
        data.write(Int(flags))
        
        data.write(String(self.text))
        
        if self.fwd_text is not None:
            data.write(String(self.fwd_text))
        
        data.write(String(self.url))
        
        data.write(Int(self.button_id))
        
        return data.getvalue()
