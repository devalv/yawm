# -*- coding: utf-8 -*-
"""Project web utils."""
import httpx

# TODO: types and annotations


class PageParser:
    """Parse page."""

    __h1_search_patterns = {"</h1": None, "1>": "</h", "/h1": "<", "h1": "</"}

    def __init__(self, chunk_iter, chunk_size):
        """Please see help(PageParser) for more info."""
        self.chunk_iter = chunk_iter
        self.chunk_size = chunk_size

        self.two_chunks = False
        self.pre_value_ind = -1
        self.post_value_ind = -1

    @staticmethod
    def find_pattern_index(value: str, chunk: str, start=0) -> int:
        """Case insensitive search `value` index in `chunk`."""
        index = chunk.find(value, start)
        if index < 0:
            index = chunk.find(value.upper(), start)
        if index > 0:
            return index
        return -1

    @staticmethod
    def rfind_pattern_index(value: str, chunk: str, start=0) -> int:
        """Case insensitive reverse search `value` index in `chunk`."""
        index = chunk.rfind(value, 0, start)
        if index < 0:
            index = chunk.rfind(value.upper(), 0, start)
        if index > 0:
            return index
        return -1

    async def get_h1_value(self) -> str:
        """Get html `h1` tag value in PageParser.chunk_iter."""
        # TODO: разнести на методы
        previous_chunk = None
        post_value_ind = -1
        pre_value_ind = -1
        two_chunks = False

        async for chunk in self.chunk_iter(chunk_size=self.chunk_size):
            # поиск завершающего тэга
            if post_value_ind == -1:
                for search_pattern in self.__h1_search_patterns:
                    post_value_ind = self.find_pattern_index(search_pattern, chunk)
                    additional_search_pattern = self.__h1_search_patterns[
                        search_pattern
                    ]
                    if (
                        post_value_ind >= 0
                        and previous_chunk  # noqa: W503
                        and additional_search_pattern  # noqa: W503
                    ):
                        # ищем окончание тэга в предыдущем чанке
                        if additional_search_pattern:
                            post_value_ind = self.rfind_pattern_index(
                                additional_search_pattern, previous_chunk
                            )
                            if post_value_ind >= 0:
                                two_chunks = True
                                break
                    elif post_value_ind >= 0:
                        break

            # поиск открывающего тэга
            # TODO: translate
            if post_value_ind >= 0 and pre_value_ind == -1:
                pre_value_ind = self.rfind_pattern_index(">", chunk, post_value_ind)
                if post_value_ind - pre_value_ind < 2:
                    pre_value_ind = -1
                    post_value_ind = -1
                elif pre_value_ind == -1:
                    pre_value_ind = self.rfind_pattern_index(
                        ">", previous_chunk, self.chunk_size
                    )
                    two_chunks = True

            # собираем результат
            if pre_value_ind >= 0 and post_value_ind >= 1:
                start = pre_value_ind + 1
                if two_chunks:
                    begin_str = previous_chunk[start:]
                    end_str = chunk[:post_value_ind]
                    return f"{begin_str}{end_str}"
                return chunk[start:post_value_ind]

            previous_chunk = chunk


async def get_product_name(url: str, chunk_size: int = 100):
    """Get product name from url."""
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            response_iter = response.aiter_text
            page_parser = PageParser(chunk_iter=response_iter, chunk_size=chunk_size)
            return await page_parser.get_h1_value()
