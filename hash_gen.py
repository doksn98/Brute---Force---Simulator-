import hashlib

passwort = " " 

hash_wert = hashlib.sha256(passwort.encode()).hexdigest()

print(f"Passwort: {passwort}")
print(f"Hash: {hash_wert}")
