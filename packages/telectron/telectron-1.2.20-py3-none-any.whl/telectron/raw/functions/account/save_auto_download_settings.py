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


class SaveAutoDownloadSettings(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``129``
        - ID: ``0x76f36233``

    Parameters:
        settings: :obj:`AutoDownloadSettings <telectron.raw.base.AutoDownloadSettings>`
        low (optional): ``bool``
        high (optional): ``bool``

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["settings", "low", "high"]

    ID = 0x76f36233
    QUALNAME = "functions.account.SaveAutoDownloadSettings"

    def __init__(self, *, settings: "raw.base.AutoDownloadSettings", low: Union[None, bool] = None, high: Union[None, bool] = None) -> None:
        self.settings = settings  # AutoDownloadSettings
        self.low = low  # flags.0?true
        self.high = high  # flags.1?true

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SaveAutoDownloadSettings":
        flags = Int.read(data)
        
        low = True if flags & (1 << 0) else False
        high = True if flags & (1 << 1) else False
        settings = TLObject.read(data)
        
        return SaveAutoDownloadSettings(settings=settings, low=low, high=high)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.low else 0
        flags |= (1 << 1) if self.high else 0
        data.write(Int(flags))
        
        data.write(self.settings.write())
        
        return data.getvalue()
