import hashlib

org_slash_repo = "agardnerIT/platform-engineering-demo"
bytes = org_slash_repo.encode()

h = hashlib.new("sha256")

h.update(bytes)
print(h.hexdigest())