# -*- coding: utf-8 -*-
"""Project web utils."""

import httpx

from core.config import CRAWLER_USER_AGENT


class PageParser:
    """Parse page by chunks in a search for the tag value.

    Attributes:
        __H1_SEARCH_PATTERNS: additional (extra) patters for searching a tag.
        chunk_iter: httpx.client iterable response (just html text).
        chunk_size: size of a feature chunks.
        __look_in_previous_chunk: if the value is located on 2 chunks.
        __prev_chunk: chunk_iter previous chunk
        __open_tag_ind: index where open tag closed, like a `>` in <h1>
        __close_tag_ind: index where closing tag starts, like a '<' in </h1>

    Note:
        1. Too small chunks can do everything worse.
        2. Closing tag is looking first.
           Closing -> Open -> Value

    """

    __H1_SEARCH_PATTERNS = {"</h1": None, "1>": "</h", "/h1": "<", "h1": "</"}

    def __init__(self, chunk_iter, chunk_size):
        """Please see help(PageParser) for more info."""
        self.chunk_iter = chunk_iter
        self.chunk_size = chunk_size
        self.__look_in_previous_chunk = False
        self.__prev_chunk = None
        self.__open_tag_ind = -1
        self.__close_tag_ind = -1

    @staticmethod
    def find_pattern_ind(value: str, chunk: str, start=0) -> int:
        """Case insensitive search `value` index in `chunk`."""
        index = chunk.find(value, start)
        if index < 0:
            index = chunk.find(value.upper(), start)
        if index > 0:
            return index
        return -1

    @staticmethod
    def rfind_pattern_ind(value: str, chunk: str, start=0) -> int:
        """Case insensitive reverse search `value` index in `chunk`."""
        index = chunk.rfind(value, 0, start)
        if index < 0:
            index = chunk.rfind(value.upper(), 0, start)
        if index > 0:
            return index
        return -1

    @property
    def close_tag_ind(self) -> int:
        """Just return private close_tag_ind."""
        return self.__close_tag_ind

    @close_tag_ind.setter
    def close_tag_ind(self, chunk: str) -> int:
        """Find a tag position in a chunk and remember index."""
        value_ind = -1
        # break if there is nothing to search
        if not chunk:
            self.__close_tag_ind = value_ind
            return
        # try to find proper index
        for pattern in self.__H1_SEARCH_PATTERNS:
            value_ind = self.find_pattern_ind(pattern, chunk)
            extra_pattern = self.__H1_SEARCH_PATTERNS[pattern]
            # logical conditions
            extra_search_needed = value_ind >= 0 and self.__prev_chunk and extra_pattern
            value_found = value_ind >= 0 and not extra_pattern
            value_cant_be_found = extra_pattern and not self.__prev_chunk
            # try to look in a previous chunk if it makes sense
            if value_found:
                break
            elif value_cant_be_found:
                value_ind = -1
            elif extra_search_needed:
                # end of a tag must be in a previous chunk
                value_ind = self.rfind_pattern_ind(extra_pattern, self.__prev_chunk)
                if value_ind >= 0:
                    self.__look_in_previous_chunk = True
                    break
        # set private value
        self.__close_tag_ind = value_ind

    @property
    def open_tag_ind(self) -> int:
        """Just return private open_tag_ind."""
        return self.__open_tag_ind

    @open_tag_ind.setter
    def open_tag_ind(self, chunk: str) -> int:
        """Find a tag position in a chunk and remember index."""
        value_ind = -1
        # break if there is nothing to search
        if not chunk:
            self.__close_tag_ind = value_ind
            return
        # try to find proper index
        if self.close_tag_ind >= 0 and value_ind == -1:
            value_ind = self.rfind_pattern_ind(">", chunk, self.close_tag_ind)
            tag_has_no_value = self.close_tag_ind - value_ind < 2
            if tag_has_no_value:
                value_ind = -1
                self.close_tag_ind = None
            elif value_ind == -1:
                value_ind = self.rfind_pattern_ind(
                    ">", self.__prev_chunk, self.chunk_size
                )
                self.__look_in_previous_chunk = True
        # set private value
        self.__open_tag_ind = value_ind

    @property
    def value_start_ind(self) -> int:
        """Index there value in chunk starting."""
        return self.open_tag_ind + 1

    @property
    def value_end_ind(self) -> int:
        """The index itself is greater for 1, but for slices ok."""
        return self.close_tag_ind

    @property
    def both_ind_found(self) -> bool:
        """If both indexes found - you can get a value."""
        return self.open_tag_ind >= 0 and self.close_tag_ind >= 1

    async def get_value(self) -> str:
        """Get html tag value from PageParser.chunk_iter."""
        async for chunk in self.chunk_iter(chunk_size=self.chunk_size):
            if self.close_tag_ind == -1:
                self.close_tag_ind = chunk
            if self.close_tag_ind >= 0 and self.open_tag_ind == -1:
                self.open_tag_ind = chunk
            if self.both_ind_found:
                # fmt: off
                if self.__look_in_previous_chunk:
                    value_from_prev_chunk = self.__prev_chunk[self.value_start_ind:]
                    value_from_curr_chunk = chunk[:self.value_end_ind]
                    value = f"{value_from_prev_chunk}{value_from_curr_chunk}"
                else:
                    value = chunk[self.value_start_ind:self.value_end_ind]
                # remove useless garbage
                if isinstance(value, str):
                    value = value.strip()
                return value
                # fmt: on
            self.__prev_chunk = chunk


async def get_product_name(url: str, chunk_size: int = 100) -> str:
    """Extract product name from url.

    Note:
        If response will be empty - product name will be None.
    """
    try:
        async with httpx.AsyncClient(
            headers={"User-Agent": CRAWLER_USER_AGENT}
        ) as client:
            async with client.stream("GET", url) as response:
                response_iter = response.aiter_text
                page_parser = PageParser(
                    chunk_iter=response_iter, chunk_size=chunk_size
                )
                return await page_parser.get_value()
    except httpx.RequestError:  # pragma: no cover
        return
