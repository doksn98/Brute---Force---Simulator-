# 🛡️ Brute Force Simulator

Ein Tool zur Veranschaulichung der Funktionsweise von Brute-Force-Angriffen und der Bedeutung von Passwortsicherheit.

## Beschreibung
Dieser Simulator demonstriert, wie automatisierte Skripte versuchen, Passwörter durch systematisches Durchprobieren von Zeichenkombinationen zu knacken. 

## Funktionen
- **Echtzeit-Simulation:** Visualisierung des Trial-and-Error-Prozesses.
- **Komplexitätsanalyse:** Berechnung der benötigten Zeit basierend auf Zeichensatz und Länge.

## Technologien
- **Sprache:** Python 
- **Konzepte:** Kryptographie-Grundlagen, Iterations-Logik, String-Manipulation.
- **Datenbank:** Passwortliste bestehend aus 10.000 deutsche Wörter.

## Nutzung
1. **Hash generieren:** Führe `python hash_gen.py` aus, gib ein Test-Passwort ein und kopiere den angezeigten Hash-Code.
2. **Simulator starten:** Führe `python brute.py` im Terminal aus.
3. **Entschlüsselung:** Füge den kopierten Hash ein und drücke Enter – das Skript generiert nun systematisch Zeichen, bis es das ursprüngliche Passwort findet.

## ⚠️ Disclaimer
Dieses Projekt wurde ausschließlich zu Bildungszwecken entwickelt.
