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

from .handler import Handler


class InlineQueryHandler(Handler):
    """The InlineQuery handler class. Used to handle inline queries.
    It is intended to be used with :meth:`~telectron.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~telectron.Client.on_inline_query` decorator.

    Parameters:
        callback (``callable``):
            Pass a function that will be called when a new InlineQuery arrives. It takes *(client, inline_query)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of inline queries to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~telectron.Client`):
            The Client itself, useful when you want to call other API methods inside the inline query handler.

        inline_query (:obj:`~telectron.types.InlineQuery`):
            The received inline query.
    """

    def __init__(self, callback: callable, filters=None):
        super().__init__(callback, filters)
