import hashlib
import time

def brute_force_simulation(target_password, wordlist_path):
    # Hash berechnen (Simuliert den Eintrag in einer Datenbank)
    target_hash = hashlib.sha256(target_password.encode()).hexdigest()
    start_time = time.time()
    versuche = 0

    print(f"\n--- Simulation gestartet ---")
    print(f"Ziel-Hash: {target_hash}")
    
    try:
        # 'errors=ignore' verhindert Abstürze bei nicht-lesbaren Zeichen in der Liste
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for word in file:
                word = word.strip()
                versuche += 1
                
                # Performance-Boost: Nur alle 5000 Zeilen drucken
                if versuche % 5000 == 0:
                    print(f"Status: {versuche} Versuche...", end="\r")
                
                guess_hash = hashlib.sha256(word.encode()).hexdigest()
                
                if guess_hash == target_hash:
                    dauer = round(time.time() - start_time, 4)
                    return f"\n\n✅ TREFFER! Passwort: '{word}'\nAnzahl Versuche: {versuche}\nDauer: {dauer} Sekunden"
                    
        return f"\n\n❌ Passwort nicht in der Liste gefunden. ({versuche} Versuche)"
    except FileNotFoundError:
        return "\nFehler: Datei nicht gefunden! Stelle sicher, dass der Pfad stimmt."

if __name__ == "__main__":
    test_pw = input("Gib das Ziel-Passwort ein: ")
    # Tipp: Nutze 'rockyou.txt' oder eine ähnliche Liste für echte Tests
    print(brute_force_simulation(test_pw, "passwoerter.txt"))
