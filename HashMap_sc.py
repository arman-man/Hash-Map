# Name: Arman Manukyan
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap
# Description: Implementation of an SC (Separate Chaining) and OA (Open Addressing) HashMap.

from DynamicArray_LinkedList import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Calculated index of the key
        index = self._hash_function(key) % self._capacity

        # If the key is not in the HashMap add a new node to the hash table at the index
        if not self.contains_key(key):
            self._buckets[index].insert(key, value)
            self._size += 1

        # If the key already exists replace it with the new node
        else:
            self._buckets[index].remove(key)
            self._buckets[index].insert(key, value)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :param: None

        :return: integer, empty buckets
        """
        count = 0
        for i in range(0, self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        :param: None

        :return: float, load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :param: None

        :return: None
        """
        for i in range(0, self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.

        :param new_capacity: integer

        :return: None
        """
        if new_capacity >= 1:

            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            # List of values in the HashMap
            valuesList = LinkedList()
            for i in range(0, self._capacity):
                if self._buckets[i].length() >= 1:
                    for item in self._buckets[i]:
                        valuesList.insert(item.key, item.value)

            # Empty the HashMap and increase the capacity
            self._buckets = DynamicArray()
            for i in range(0, new_capacity):
                self._buckets.append(LinkedList())
            self._capacity = new_capacity
            self._size = 0

            # Re-add the values back into the HashMap
            for item in valuesList:
                self.put(item.key, item.value)

    def get(self, key: str):
        """
        Returns the value associated with the given key.

        :param key: string

        :return: any object or None
        """
        index = self._hash_function(key) % self._capacity
        if self.contains_key(key):
            return self._buckets[index].contains(key).value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map,
        or False if the key is not in the hash map.

        :param key: string

        :return: bool
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.

        :param key: string

        :return: None
        """
        index = self._hash_function(key) % self._capacity
        if self.contains_key(key):
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair.

        :param: None

        :return: DynamicArray
        """
        returnArr = DynamicArray()
        for i in range(0, self._capacity):
            for node in self._buckets[i]:
                returnArr.append((node.key, node.value))
        return returnArr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing a dynamic array comprising the mode value(s) of the array,
    and an integer that represents the frequency. With O(N) time complexity.

    :param da: DynamicArray

    :return: Tuple of (DynamicArray, integer)
    """
    # Using hash_function_2 since assuming all values are strings
    map = HashMap(da.length(), hash_function_2)

    numModes = DynamicArray()
    frequency = 0

    for i in range(0, da.length()):
        key = da[i]
        value = map.get(key)
        if value:
            value += 1
        elif not value:
            value = 1
        map.put(key, value)

        # Update numModes and frequency
        if value > frequency:
            numModes = DynamicArray()
            numModes.append(key)
            frequency = value

        # Check for more multiple modes
        elif value is frequency:
            numModes.append(key)

    return numModes, frequency


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
