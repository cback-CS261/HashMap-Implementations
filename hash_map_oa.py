# Name: Chance Back
# OSU Email: backc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/22
# Description:  This program contains a class for implementing hash maps that 
#               utilizes open addressing to deal with hash collisions. The 
#               underlying data structures used are imported Dynamic Array and 
#               Linked List classes. Two hash functions are also imported as 
#               well.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
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

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the given key already 
        exists in the hash map, its associated value is replaced with the new 
        value. If the given key is not in the hash map, a new key / value pair 
        is added.

        :param key:         key to be used in the key / value pair
        :param value:       value to be used in the key / value pair

        :return:        None
        """
        # Resizes table if load factor gets too high by default
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Find the initial index and create variable for quadratic probing
        hash = self._hash_function(key)
        init_index = hash % self._capacity
        j = 0

        # Probe for the correct index and insert key / value pair when found
        for _ in range(self._capacity):
            quad_index = (init_index + j**2) % self._capacity
            bucket = self._buckets.get_at_index(quad_index)
            if not bucket or bucket.is_tombstone:
                entry = HashEntry(key, value)
                self._buckets.set_at_index(quad_index, entry)
                self._size += 1
                return
            elif bucket.key == key:
                bucket.value = value
                return
            
            # Increment quadratic probing variable
            j += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        :return:    hash table load factor
        """
        # Calculate load factor
        load_factor = self._size / self._capacity

        # Return load factor
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        
        :return:    empty buckets in the hash table
        """
        # Calculate empty buckets
        empty_buckets = self._capacity - self._size

        # Return empty buckets
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value
        pairs will remain in the new hash map, and all hash table links will be 
        rehashed.

        :param new_capacity:    new capacity of the hash map

        :return:                None
        """
        # Check if new capacity is valid
        if new_capacity < self._size:
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
            self._buckets.append(None)

        self._size = 0

        # Iterate through all buckets in old array and rehash values to new table
        for num in range(old_capacity):
            bucket = old_map.get_at_index(num)
            if bucket and not bucket.is_tombstone:
                self.put(bucket.key, bucket.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in 
        the hash map, the method returns None.

        :param key: key to search for in hash map

        :return:    value associated with key or None if key not found
        """
        # Find the initial index and create variable for quadratic probing
        hash = self._hash_function(key)
        init_index = hash % self._capacity
        j = 0

        # Probe for the correct key / value pair and return value if found
        for _ in range(self._capacity):
            quad_index = (init_index + j**2) % self._capacity
            bucket = self._buckets.get_at_index(quad_index)
            if not bucket:
                return
            elif not bucket.is_tombstone and key == bucket.key:
                return bucket.value
            
            # Increment quadratic probing variable
            j += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns 
        False.

        :param key: key to be searched for

        :return: True/False depending on if key is found
        """
        # Find the initial index and create variable for quadratic probing
        hash = self._hash_function(key)
        init_index = hash % self._capacity
        j = 0

        # Probe for the correct key and return True if found else return False
        for _ in range(self._capacity):
            quad_index = (init_index + j**2) % self._capacity
            bucket = self._buckets.get_at_index(quad_index)
            if not bucket:
                return False
            elif not bucket.is_tombstone and key == bucket.key:
                return True

            # Increment quadratic probing variable
            j += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map if it
        is in the hash map.

        :param key: key of key / value pair to be removed from hash map

        :return:    None
        """
        # Find the initial index and create variable for quadratic probing
        hash = self._hash_function(key)
        init_index = hash % self._capacity
        j = 0

        # Probe for the correct key and return remove if found
        for _ in range(self._capacity):
            quad_index = (init_index + j**2) % self._capacity
            bucket = self._buckets.get_at_index(quad_index)
            if not bucket:
                return
            elif not bucket.is_tombstone and key == bucket.key:
                # Remove by setting .is_tombstone to True and reducing map size
                bucket.is_tombstone = True
                self._size -= 1

            # Increment quadratic probing variable
            j += 1


    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying 
        hash table capacity.

        :return:    None
        """
        # Empty contents of array while maintaining compacity
        for num in range(self._capacity):
            self._buckets.set_at_index(num, None)
        
        # Reset size
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a 
        key / value pair stored in the hash map.

        :return:    dynamic array key / value pair tuples
        """
        # Iterate through all buckets in hash map and append key / value tuple
        key_val_arr = DynamicArray()
        for num in range(self._capacity):
            bucket = self._buckets.get_at_index(num)
            if bucket and not bucket.is_tombstone:
                key_val_pair = (bucket.key, bucket.value)
                key_val_arr.append(key_val_pair)

        # Return array of key / value pairs
        return key_val_arr


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
