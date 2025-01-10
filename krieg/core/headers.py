from typing import List, Tuple, Dict


class Header:
    def __init__(self, headers: List[Tuple[bytes, bytes]] = None):
        """
        Initializes the Header class.
        """
        self.headers: List[Tuple[bytes, bytes]] = []
        self.headers_dict: Dict[bytes, bytes] = {}

        if headers:
            self._initialize_from_scope(headers)

    def _initialize_from_scope(self, headers: List[Tuple[bytes, bytes]]):
        """
        Populates the headers from a given scope.

        :param headers: A list of headers as byte tuples from the ASGI scope.
        """
        for name, value in headers:
            self.add_header(name.decode("utf-8"), value.decode("utf-8"))

    def add_header(self, name: str, value: str):
        """
        Adds a header. The header names and values are converted to bytes.

        :param name: The name of the header.
        :param value: The value of the header.
        :raises ValueError: If the header name or value is empty.
        """
        if not name or not value:
            raise ValueError("Header name and value cannot be empty.")

        name_bytes = name.encode("utf-8")
        value_bytes = value.encode("utf-8")
        self.headers_dict[name_bytes] = value_bytes
        self.headers.append((name_bytes, value_bytes))

    def remove_header(self, name: str):
        """
        Removes the header with the given name.

        :param name: The name of the header to be removed.
        """
        name_bytes = name.encode("utf-8")

        if name_bytes in self.headers_dict:
            del self.headers_dict[name_bytes]
            self.headers = list(self.headers_dict.items())

    def get_headers(self) -> List[Tuple[bytes, bytes]]:
        """
        Returns the list of headers.

        :return: List of headers.
        """
        return self.headers

    def get_header(self, name: str) -> bytes:
        """
        Gets the value of a specific header.

        :param name: The name of the header.
        :return: The value of the header in bytes, or None if not found.
        """
        name_bytes = name.encode("utf-8")
        return self.headers_dict.get(name_bytes)

    def set_header(self, name: str, value: str):
        """
        Sets or updates a specific header.

        :param name: The name of the header.
        :param value: The value of the header.
        """
        self.remove_header(name)
        self.add_header(name, value)
