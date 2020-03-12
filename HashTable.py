class HashNode:
    """
    DO NOT EDIT
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __repr__(self):
        return #f"HashNode({self.key}, {self.value})"

class HashTable:
    """
    Hash table class, utilizes double hashing for conflicts
    """

    def __init__(self, capacity=4):
        """
        DO NOT EDIT
        Initializes hash table
        :param tableSize: size of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None]*capacity


    def __eq__(self, other):
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True


    def __repr__(self):
        pass


    def hash_function(self, x):
        """
        ---DO NOT EDIT---

        Converts a string x into a bin number for our hash table
        :param x: key to be hashed
        :return: bin number to insert hash item at in our table, -1 if x is an empty string
        """
        if not x:
            return -1
        hashed_value = 0

        for char in x:
            hashed_value = 181 * hashed_value + ord(char)

        return hashed_value % self.capacity


    def insert(self, key, value):
        """
        inserts value at appropriate bucket
        :param key: key to be inserted
        :param value: value associated with key
        :return: leave function
        """
        #get bucket
        bucket = self.hash_function(key)
        #key is empty string no insert
        if bucket == -1:
            return
        ins_node = HashNode(key, value)
        # if the bucket is empty, the item can be inserted index
        if self.table[bucket] is None:
            self.table[bucket] = ins_node
            self.size += 1
            load_factor = self.size / self.capacity
            if load_factor > 0.75:
                self.grow()
            return
        else:
            # the bucket was occupied, continue probing to next index in table.
            bucket = self.quadratic_probe(key)
            if bucket is None:
                return
            if self.table[bucket] is None:
                self.table[bucket] = ins_node
                self.size += 1
                load_factor = self.size / self.capacity
                if load_factor > 0.75:
                    self.grow()
                return
            elif self.table[bucket].key == key:
                #update to current value
                self.table[bucket].value = value
                return
        # the entire table was full and the key could not be inserted.
        return

    def quadratic_probe(self, key):
        """
        search for bucket with key in table if not
        found apply algorithm until empty bucket found
        :param key: key for algorithm
        :return: either the bucket containg key or open bucket
        """
        if key == "":
            return -1
        bucket = self.hash_function(key)
        #first search for key in array
        for i in range(len(self.table)):
            # Compute the bucket index
            bucket = (bucket + i**2) % self.capacity
            #bucket is full - check if filled with key
            if self.table[bucket] is not None:
                if self.table[bucket].key == key:
                    return bucket
        bucket = self.hash_function(key)
        #if that fails search for empty location
        for i in range(len(self.table)):
            # Compute the bucket index
            bucket = (bucket + i**2) % self.capacity
            #bucket is full - check if filled with key
            if self.table[bucket] is None:
                return bucket
                
    def find(self, key):
        """
        finds the provided key in table
        :param key: key to find
        :return: node containing key, false otherwise
        """
        bucket = self.quadratic_probe(key)
        if self.table[bucket] is None:
            return False
        if self.table[bucket].key == key:
            return self.table[bucket]
        else:
            return False

    def lookup(self, key):
        """
        finds the provided key in table
        :param key: key to lookup
        :return: value associated with key, false otherwise
        """
        bucket = self.quadratic_probe(key)
        if bucket is None:
            return False
        if self.table[bucket] is None:
            return False
        if self.table[bucket].key == key:
            return self.table[bucket].value
        else:
            return False

    def delete(self, key):
        """
        remove node with key from table
        :param key: key to be deleted
        :return: leave function
        """
        bucket = self.quadratic_probe(key)
        if self.table[bucket] is None:
            return
        if self.table[bucket].key == key:
            self.table[bucket] = None
            self.size -= 1
        else:
            return
        
    def grow(self):
        """
        double capacity of table
        return: no return
        """
        self.capacity = self.capacity * 2
        self.rehash()
        
    def rehash(self):
        """
        creates new table and rehashes values
        :return: no return
        """
        new_table = [None]*self.capacity
        temp_table = self.table
        self.table = new_table
        self.size = 0
        for i in range(len(temp_table)):
            nodel = temp_table[i]
            if nodel is not None:
                self.insert(nodel.key, nodel.value)

def string_difference(string1, string2):
    """
    compare the characters of two strings
    by using hash tables
    :param string1: string to be compared
    :param string2: string to be compared
    :return: set containing difference of strings
    """
    Hash1 = HashTable()
    Hash2 = HashTable()
    for ch in string1:
        nodel = Hash1.find(ch)
        if nodel is not False:
            nodel.value += 1
        else:
            Hash1.insert(ch, 1)
    for ch in string2:
        nodel = Hash2.find(ch)
        if nodel is not False:
            nodel.value += 1
        else:
            Hash2.insert(ch, 1)
    out_set = set()
    for item in Hash1.table:
        if item is not None:
            val = Hash2.lookup(item.key)
            if val is not False:
                if item.value > val:
                    amount = item.value - val
                    val_str = amount * item.key
                    out_set.add(val_str)
                else:
                    amount = val - item.value
                    val_str = amount * item.key
                    out_set.add(val_str)
            else:
                val_str = item.key * item.value
                out_set.add(val_str)
    for item in Hash2.table:
        if item is not None:
            val = Hash1.lookup(item.key)
            if val is False:
                val_str = item.key * item.value
                out_set.add(val_str)
    if '' in out_set:
        out_set.remove('')  
    return out_set
    