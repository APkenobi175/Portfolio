import hashlib
myMessagfe = "hello world"
hasher = hashlib.sha256()
hasher.update(bytes(myMessagfe, 'utf-8'))

print(hasher.hexdigest())