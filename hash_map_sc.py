# Name: Chance Back
# OSU Email: backc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/22
# Description:  This program contains a class for implementing hash maps that 
#               utilize chaining to deal with hash collisions. The underlying 
#               data structures used are imported Dynamic Array and Linked List 
#               classes. Two hash functions are also imported as well. The
#               program also contains a separate function for finding the mode
#               of a dynamic array using the hash map.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object, update_size: bool=True) -> None:
        """
        Updates the key / value pair in the hash map. If the given key already 
        exists in the hash map, its associated value is replaced with the new 
        value. If the given key is not in the hash map, a new key / value 
        pair is added.

        :param key:     key to be used in the key / value pair
        :param value:   value to be used in the key / value pair

        :return:        None
        """
        # Determine the index of the given key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Find the bucket the key / value pair will be located
        bucket = self._buckets.get_at_index(index)

        # Check if bucket contains key / value pair and update or add accordingly
        node = bucket.contains(key)
        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

        # Resizes table if load factor gets too high by default
        if update_size and self.table_load() > 8:
            new_capacity = self._size * 2
            self.resize_table(new_capacity)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return:    empty buckets in the hash table
        """
        # Iterate through buckets tracking the empty ones
        empty_buckets = 0
        for num in range(self._capacity):
            bucket = self._buckets.get_at_index(num)
            if bucket.length() == 0:
                empty_buckets += 1

        # Return the number of empty buckets
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        :return:    load factor of hash table
        """
        # Calculate load factor
        load_factor = self._size / self._capacity

        # Return load factor
        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying 
        hash table capacity.

        :return:    None
        """
        # Iterate through buckets and clear out the underlying linked lists
        for num in range(self._capacity):
            self._buckets.set_at_index(num, LinkedList())
        
        # Reset size to zero when finished
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value
        pairs will remain in the new hash map, and all hash table links will be 
        rehashed.

        :param new_capacity:    new capacity of the hash map

        :return:                None
        """
        # Check if new capacity is valid
        if new_capacity < 1:
            return

        # Store old array and capacity
        old_map = self._buckets
        old_capacity = self._capacity

        # Create new hash map with updated capacity and size
        self._buckets = DynamicArray()

        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

        # Iterate through all buckets in old array and rehash values to new table
        for num in range(old_capacity):
            bucket = old_map.get_at_index(num)
            for node in bucket:
                self.put(node.key, node.value, False)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in 
        the hash map, the method returns None.

        :param key: key to search for in hash map

        :return:    value associated with key or None if key not found
        """
        # Determine the index of the given key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Find the bucket the key / value pair will be located
        bucket = self._buckets.get_at_index(index)

        # Check if bucket contains key / value pair and return value if found
        node = bucket.contains(key)
        if node:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.

        :param key: key to be searched for in hash map

        :return:    True/False depending on if key is found
        """
        # Check if hash map is empty
        if self._size == 0:
            return False

        # Determine the index of the given key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Find the bucket the key / value pair will be located
        bucket = self._buckets.get_at_index(index)

        # Check if bucket contains key / value pair and return results
        node = bucket.contains(key)
        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If 
        the key is not in the hash map, the method does nothing.

        :param key: key of key / value pair to be removed from hash map

        :return:    None
        """
        # Determine the index of the given key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Find the bucket the key / value pair will be located
        bucket = self._buckets.get_at_index(index)

        # Check if bucket contains key / value and remove if found
        result = bucket.remove(key)
        if result:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a 
        key / value pair stored in the hash map.

        :return:    dynamic array containing all key / value pairs in hash map
        """
        # Iterate through all buckets in hash map and append key / value tuple
        key_val_arr = DynamicArray()
        for num in range(self._capacity):
            bucket = self._buckets.get_at_index(num)
            for node in bucket:
                key_val_pair = (node.key, node.value)
                key_val_arr.append(key_val_pair)

        # Return array of key / value pairs
        return key_val_arr

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing, in this order, a dynamic array comprising the 
    mode (most occurring) value/s of the array, and an integer that represents 
    the highest frequency (how many times they appear).

    :param da:  dynamic array to used to search for mode

    :return:    tuple containing a new dynamic array of most occuring values 
                and an integer representing the highest frequency
    """
    #Initialize hash map to store frequencies
    map = HashMap()

    # Iterate through dynamic array tracking frequency of values in hash map
    for num in range(da.length()):
        key = da.get_at_index(num)
        current_freq = map.get(key)

        if not current_freq:
            current_freq = 0
        
        map.put(key, current_freq + 1)

    # Convert hash map of frequencies into array
    map_arr = map.get_keys_and_values()

    # Iterate through array of frequencies and find/store the mode(s)
    highest_freq = 0
    for num in range(map_arr.length()):
        key_val_pair = map_arr.get_at_index(num)
        if key_val_pair[1] > highest_freq:
            highest_freq = key_val_pair[1]
            modes_arr = DynamicArray()
            modes_arr.append(key_val_pair[0])
        elif key_val_pair[1] == highest_freq:
            modes_arr.append(key_val_pair[0])

    # Return the mode(s) and frequency
    return (modes_arr, highest_freq)

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

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
