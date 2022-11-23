# Name: Arman Manukyan
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Description: Implementation of an SC (Separate Chaining) and OA (Open Addressing) HashMap.

from DynamicArray_LinkedList import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Creates or updates the key/value pair in the hash map.

        :param key: string
        :param value: any object

        :return: None
        """
        # Double the capacity if size >= capacity
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)
        index = hash % self._capacity
        k = 0
        while self._buckets[index] is not None:
            # Stops function if index is not a tombstone and index already contains the key
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                self._buckets[index].value = value
                return

            # Updates the key/value pair and stops the function if the index is the tombstone
            elif self._buckets[index].is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return

            # Next iteration
            k += 1
            index = (hash + (k ** 2)) % self._capacity

        # Add the new key/value pair
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        :param: None

        :return: float, load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :param: None

        :return: integer, empty buckets
        """
        count = 0
        for i in range(0, self._capacity):
            if self._buckets[i] is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.

        :param new_capacity: integer

        :return: None
        """
        if new_capacity >= self._size:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            # Creates a temporary hash map
            tempMap = HashMap(new_capacity, self._hash_function)

            # Fills the temp hash map with current hash map values
            for i in range(0, self._capacity):
                if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                    tempMap.put(self._buckets[i].key, self._buckets[i].value)

            # Updates the current hash map to the temp hash map
            self._capacity = tempMap._capacity
            self._buckets = tempMap._buckets

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.

        :param key: string

        :return: any object
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        k = 0
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return self._buckets[index].value

            k += 1
            index = (hash + (k ** 2)) % self._capacity

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map,
        or False if the key is not in the hash map.

        :param key: string

        :return: bool
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        k = 0
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return True

            k += 1
            index = (hash + (k ** 2)) % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.

        :param key: string

        :return: None
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        k = 0
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                self._buckets[index].is_tombstone = True
                self._size -= 1
            k += 1
            index = (hash + (k ** 2)) % self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :param: None

        :return: None
        """
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(0, self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair.

        :param: None

        :return: DynamicArray
        """
        returnArr = DynamicArray()
        for i in range(0, self._capacity):
            if self._buckets[i] is not None:
                if not self._buckets[i].is_tombstone:
                    returnArr.append((self._buckets[i].key, self._buckets[i].value))
        return returnArr

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.

        :param: None

        :return: self
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the iterator.

        :param: None

        :return: any Object
        """
        try:
            item = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1

        try:
            if not item.is_tombstone:
                return item
        except AttributeError:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
