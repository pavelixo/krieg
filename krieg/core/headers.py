from typing import List, Tuple
from krieg.utils.datastructures import OrderedSet, MultiValueDict


class Header:
    def __init__(self, headers: List[Tuple[bytes, bytes]] = None):
        """
        Initializes the Header class, optionally with a list of headers.

        :param headers: A list of headers in the form of tuples of bytes (name, value).
        """
        self.headers = OrderedSet()  # Using OrderedSet to maintain header order
        self.headers_dict = MultiValueDict()  # Using MultiValueDict for multiple values per key

        if headers:
            self._initialize_from_scope(headers)

    def _initialize_from_scope(self, headers: List[Tuple[bytes, bytes]]):
        """
        Populates headers from the provided scope.

        :param headers: A list of headers in the form of tuples of bytes (name, value).
        """
        for name, value in headers:
            self.add_header(name.decode("utf-8"), value.decode("utf-8"))

    def add_header(self, name: str, value: str):
        """
        Adds a header. The header name and value are converted to bytes.

        :param name: The name of the header.
        :param value: The value of the header.
        :raises ValueError: If the header name or value is empty.
        """
        if not name or not value:
            raise ValueError("Header name and value cannot be empty.")

        name_bytes = name.encode("utf-8")
        value_bytes = value.encode("utf-8")
        self.headers.add((name_bytes, value_bytes))  # Add to OrderedSet
        self.headers_dict.add(name_bytes, value_bytes)  # Add to MultiValueDict for multiple values

    def remove_header(self, name: str):
        """
        Removes the header with the provided name.

        :param name: The name of the header to be removed.
        """
        name_bytes = name.encode("utf-8")

        if name_bytes in self.headers_dict:
            del self.headers_dict[name_bytes]
            self.headers = OrderedSet([item for item in self.headers if item[0] != name_bytes])  # Update OrderedSet

    def get_headers(self) -> List[Tuple[bytes, bytes]]:
        """
        Returns the list of headers.

        :return: A list of headers as tuples (name, value).
        """
        return list(self.headers)

    def get_header(self, name: str) -> List[bytes]:
        """
        Gets the values of a specific header.

        :param name: The name of the header.
        :return: A list of values for the header, or an empty list if not found.
        """
        name_bytes = name.encode("utf-8")
        return self.headers_dict.get(name_bytes)  # Returns all values for the header

    def set_header(self, name: str, value: str):
        """
        Sets or updates a specific header.

        :param name: The name of the header.
        :param value: The value of the header.
        """
        self.remove_header(name)  # Remove any existing header with the same name
        self.add_header(name, value)  # Add the new header
