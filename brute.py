import hashlib
import time

def brute_force_simulation(target_password, wordlist_path):
    # Erstellt den Ziel-Hash für die Simulation
    target_hash = hashlib.sha256(target_password.encode()).hexdigest()
    start_time = time.time()
    versuche = 0

    print(f"\n--- Simulation gestartet für: {target_password} ---")
    
    try:
        with open(wordlist_path, 'r') as file:
            for word in file:
                word = word.strip()
                versuche += 1
                
                # Echtzeit-Simulation
                if versuche % 10 == 0:
                    print(f"Prüfe: {word}...", end="\r")
                
                guess_hash = hashlib.sha256(word.encode()).hexdigest()
                
                if guess_hash == target_hash:
                    dauer = round(time.time() - start_time, 4)
                    return f"\n\n✅ Erfolg! Passwort '{word}' nach {versuche} Versuchen gefunden.\nZeit: {dauer} Sekunden."
                    
        return f"\n\n❌ Passwort nicht in der Liste gefunden. ({versuche} Versuche)"
    except FileNotFoundError:
        return "\nFehler: 'passwoerter.txt' fehlt! Bitte erstelle die Datei im selben Ordner."


if __name__ == "__main__":
    test_pw = input("Gib ein Test-Passwort ein, das simuliert werden soll: ")
    print(brute_force_simulation(test_pw, "passwoerter.txt"))