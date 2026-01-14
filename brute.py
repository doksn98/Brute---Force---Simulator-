import hashlib
import time


def brute_force_simulation(target_hash, wordlist_path):
    start_time = time.time()
    versuche = 0

    
    print(f"\n--- Simulation gestartet für Hash: {target_hash} ---")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for word in file:
                word = word.strip()
                versuche += 1
                
                if versuche % 5000 == 0:
                    print(f"Status: {versuche} Versuche...", end="\r")
                
                guess_hash = hashlib.sha256(word.encode()).hexdigest()
                
                if guess_hash == target_hash:
                    dauer = round(time.time() - start_time, 4)
                    return f"\n\n✅ TREFFER! Das Passwort für den Hash ist: '{word}'\nZeit: {dauer}s"
                    
        return f"\n\n❌ Hash nicht geknackt. ({versuche} Versuche)"
    except FileNotFoundError:
        return "\nFehler: Datei nicht gefunden!"

if __name__ == "__main__":
    target_input = input("SHA256-Hash eingeben: ").strip().lower()
    print(brute_force_simulation(target_input, "passwoerter.txt"))

