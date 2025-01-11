from collections import OrderedDict, defaultdict


class OrderedSet:
    def __init__(self):
        # Initialize with an ordered dictionary to maintain insertion order
        self._data = OrderedDict()

    def add(self, value):
        """Adds a value to the set, maintaining the insertion order."""
        self._data[value] = None

    def remove(self, value):
        """Removes a value from the set."""
        if value in self._data:
            del self._data[value]
        else:
            raise KeyError(f"{value} not found in OrderedSet")

    def __contains__(self, value):
        """Checks if a value is in the set."""
        return value in self._data

    def __iter__(self):
        """Allows iteration over the elements in the OrderedSet."""
        return iter(self._data)

    def __len__(self):
        """Returns the number of elements in the OrderedSet."""
        return len(self._data)

    def __repr__(self):
        """String representation of the OrderedSet."""
        return f"OrderedSet({list(self._data.keys())})"


class MultiValueDictKeyError(KeyError):
    def __init__(self, key):
        self.key = key
        # Custom error message for multi-value dictionaries
        super().__init__(f"Key {key} does not exist in the multi-value dictionary")


class MultiValueDict:
    def __init__(self):
        # Uses defaultdict to store multiple values for each key
        self._data = defaultdict(list)

    def add(self, key, value):
        """Adds a value to the key, maintaining multiple values."""
        self._data[key].append(value)

    def get(self, key):
        """Returns all values for a key."""
        return self._data.get(key, [])

    def getlist(self, key):
        """Returns all values associated with a key as a list."""
        return self._data.get(key, [])

    def __contains__(self, key):
        """Checks if a key exists in the dictionary."""
        return key in self._data

    def __getitem__(self, key):
        """Returns all values for a key."""
        if key in self._data:
            return self._data[key]
        else:
            raise MultiValueDictKeyError(key)

    def items(self):
        """ Iterate through the dictionary and yield key-value pairs """
        for key, values in self._data.items():
            for value in values:
                yield key, value

    def __iter__(self):
        """ Return the generator from the items method """
        return self.items()

    def __repr__(self):
        """String representation of the dictionary."""
        return f"MultiValueDict({dict(self._data)})"


class ImmutableList:
    def __init__(self, items):
        # Initialize with an immutable tuple to store the items
        self._data = tuple(items)

    def __getitem__(self, index):
        """Accesses an item in the immutable list."""
        return self._data[index]

    def __iter__(self):
        """Allows iteration over the elements in the immutable list."""
        return iter(self._data)

    def __len__(self):
        """Returns the size of the immutable list."""
        return len(self._data)

    def __repr__(self):
        """String representation of the immutable list."""
        return f"ImmutableList({self._data})"


class DictWrapper:
    def __init__(self, data=None):
        """Initializes the wrapper with a dictionary."""
        self._data = data if data is not None else {}

    def __getitem__(self, key):
        """Gets a value from the dictionary."""
        return self._data[key]

    def __setitem__(self, key, value):
        """Sets a value in the dictionary."""
        self._data[key] = value

    def __delitem__(self, key):
        """Removes a key from the dictionary."""
        del self._data[key]

    def get(self, key, default=None):
        """Gets a value with a default if the key does not exist."""
        return self._data.get(key, default)

    def __repr__(self):
        """String representation of the wrapped dictionary."""
        return f"DictWrapper({self._data})"
