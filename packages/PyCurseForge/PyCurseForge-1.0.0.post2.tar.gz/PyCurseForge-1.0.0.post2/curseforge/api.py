"""
The MIT License (MIT)

Copyright (c) 2021 XuaTheGrate

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from typing import Any, Generic, NamedTuple, TypeVar
from urllib.parse import urlencode

import requests

from .enums import SortType
from .models.addon import Addon
from .models.category import Category

__all__ = ["Minecraft", "custom_interface"]


T = TypeVar("T")
class Interface(Generic[T]):
    BASE_URL = "https://addons-ecs.forgesvc.net/api/v2"

    def __init__(self, game_id: int, sections: T) -> None:
        self.game_id = game_id

        self._session = requests.Session()
        # we have to spoof a user agent or the api will not let us access it
        self._session.headers["User-Agent"] = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
        self._categories: dict[int, Category] = {}

        self.section_ids: T = sections

    def _store_category(self, data: dict[str, Any]) -> Category:
        if (id := data['categoryId']) in self._categories:
            return self._categories[id]
        category = Category(data)
        self._categories[id] = category
        return category

    def get_category(self, id: int) -> Category | None:
        return self._categories.get(id)

    @property
    def categories(self) -> list[Category]:
        return list(self._categories.values())

    def close(self) -> None:
        self._session.close()

    def __del__(self) -> None:
        self.close()

    def get_addon(self, id: int) -> Addon:
        data = self._session.get(self.BASE_URL + f"/addon/{id}")
        data.raise_for_status()
        return Addon(self, data.json())

    def get_addons(self, *ids: int) -> list[Addon]:
        data = self._session.post(self.BASE_URL + "/addon", json=list(ids))
        data.raise_for_status()
        return [Addon(self, d) for d in data.json()]

    def search(self, name: str | None = None, *,
        section_id: int = 6,
        category: Category | None = None,
        game_version: str | None = None,
        index: int = 0,
        per_page: int = 25,
        sort: SortType = SortType.FEATURED
    ) -> list[Addon]:
        params: dict[str, Any] = {"gameId": self.game_id, "sectionId": section_id,
                                  "index": index, "pageSize": per_page, "sort": sort.value}
        if name:
            params['searchFilter'] = name
        if category:
            params['categoryId'] = category.id
        if game_version:
            params['gameVersion'] = game_version

        url = self.BASE_URL + "/addon/search?" + urlencode(params)
        data = self._session.get(url)
        data.raise_for_status()
        return [Addon(self, d) for d in data.json()]


def Minecraft():
    sections = NamedTuple("Minecraft", [('mods', int), ('modpacks', int), ('texture_packs', int), ('worlds', int)])
    return Interface(432, sections(6, 4471, 12, 17))

def custom_interface(game_id: int, section_ids: T) -> Interface[T]:
    return Interface[T](game_id, section_ids)