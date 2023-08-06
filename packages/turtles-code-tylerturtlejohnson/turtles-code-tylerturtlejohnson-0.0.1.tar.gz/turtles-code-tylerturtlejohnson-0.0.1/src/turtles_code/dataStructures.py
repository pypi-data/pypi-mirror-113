class HashTable:

	def __init__(self, size):
		self.size = size
		self.hash_table = self.create_buckets()

	def create_buckets(self):
		return [[] for _ in range(self.size)]

        def hash_key(self, key):
            return hash(key) % self.size

        def get_bucket(self, key):
            return self.hash_table[self.hash_key(key)]

        def find_key(self, bucket, key):
            for index, record in enumerate(bucket):
                record_key, record_val = record

                if record_key == key:
                    return True
                else:
                    return False

	def set(self, key, val):
		
		bucket = self.get_bucket(key)

		if self.find_key(bucket, key):
			bucket[index] = (key, val)
		else:
			bucket.append((key, val))

	def get(self, key):
		
	    bucket = self.get_bucket(key)

	    if self.find_key(bucket, key):
                for index, record in enumerate(bucket):
                    record_key, record_val = record
		    return record_val
	    else:
		return "No record found"

	def delete(self, key):
		
	    bucket = self.get_bucket(key)

	    if self.find_key(bucket, key):
                for index, record in enumerate(bucket):
		    bucket.pop(index)
	    return

	def __str__(self):
	    return "".join(str(item) for item in self.hash_table)

        def __getitem__(self, key):
            return self.get(key)

        def __setitem__(self, key, val):
            return self.set(key, val)

