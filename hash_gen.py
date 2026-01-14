import hashlib

passwort = "geheim123" 

hash_wert = hashlib.sha256(passwort.encode()).hexdigest()

print(f"Passwort: {passwort}")
print(f"Zu kopierender Hash: {hash_wert}")
