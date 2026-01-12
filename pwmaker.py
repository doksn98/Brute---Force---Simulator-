#!/usr/bin/env python3
"""pwmaker.py — erzeugt große Passwortlisten für Testzwecke.

Features:
- CLI-Parameter: --count, --length, --charset, --custom-charset, --output, --progress
- Option für eindeutige Passwörter (--unique)
- Option, ein bekanntes Test-Passwort einzufügen (--known)
- Nutzt `secrets` für Zufallszahlen
"""

import argparse
import string
import secrets
import sys
import math
from time import time

CHARSET_PRESETS = {
    'letters': string.ascii_letters,
    'digits': string.digits,
    'letters_digits': string.ascii_letters + string.digits,
    'punct': string.punctuation,
    'all': string.ascii_letters + string.digits + string.punctuation,
}


def parse_args():
    p = argparse.ArgumentParser(description='Erzeuge eine Passwortliste für Brute-Force-Tests')
    p.add_argument('--count', '-c', type=int, default=1000000, help='Anzahl der Passwörter (Standard: 1_000_000)')
    p.add_argument('--length', '-l', type=int, default=8, help='Länge der Passwörter (Standard: 8)')
    p.add_argument('--charset', choices=list(CHARSET_PRESETS.keys()) + ['custom'], default='letters_digits',
                   help='Auswahl des Zeichensatzes')
    p.add_argument('--custom-charset', default='', help='Eigener Zeichensatz, verwendet mit --charset custom')
    p.add_argument('--wordlist', default=None, help='Pfad zu einer Wortliste (eine Wort pro Zeile). Wenn gesetzt, werden Passwörter aus dieser Liste gezogen')
    p.add_argument('--use-german', action='store_true', help="Benutze die eingebaute 'german_words.txt' Wortliste")
    p.add_argument('--unique', action='store_true', help='Sichere, dass alle Passwörter eindeutig sind (benötigt mehr RAM)')
    p.add_argument('--known', default=None, help='Ein bekanntes Passwort einfügen (z.B. zum Testen)')
    p.add_argument('--output', '-o', default='passwoerter.txt', help='Ausgabedatei (Standard: passwoerter.txt)')
    p.add_argument('--progress', type=int, default=100000, help='Fortschrittsanzeige alle N Einträge (0=aus)')
    return p.parse_args()


def main():
    args = parse_args()

    if args.charset == 'custom' and not args.custom_charset:
        print("Fehler: --custom-charset muss angegeben werden, wenn --charset custom gewählt ist.")
        sys.exit(1)

    # Falls Wortliste oder eingebaute deutsche Liste verwendet werden soll
    use_wordlist = False
    words = None

    if args.use_german:
        args.wordlist = 'german_words.txt'

    if args.wordlist:
        use_wordlist = True
        try:
            with open(args.wordlist, 'r', encoding='utf-8') as wl:
                words = [w.strip() for w in wl if w.strip()]
        except FileNotFoundError:
            print(f"Fehler: Wortliste '{args.wordlist}' nicht gefunden.")
            sys.exit(1)

        if not words:
            print("Fehler: Wortliste enthält keine gültigen Einträge.")
            sys.exit(1)

        if args.unique and args.count > len(words):
            print(f"Fehler: Nicht genug einzigartige Wörter ({len(words)}) in der Wortliste für {args.count} eindeutige Passwörter.")
            sys.exit(1)

    # Charset-basierten Platz prüfen (nur relevant, wenn keine Wortliste verwendet wird)
    charset = (args.custom_charset if args.charset == 'custom' else CHARSET_PRESETS[args.charset])
    if not use_wordlist:
        pw_space = len(charset) ** args.length
        if args.unique and args.count > pw_space:
            print(f"Fehler: Nicht genug mögliche Kombinationen ({pw_space}) für {args.count} eindeutige Passwörter.")
            sys.exit(1)

    seen = set() if args.unique else None

    total = args.count
    written = 0
    start = time()

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            # Falls ein bekanntes Passwort angegeben ist, schreibe es zuerst
            if args.known:
                f.write(args.known + '\n')
                written += 1
                if seen is not None:
                    seen.add(args.known)

            # Wenn eine Wortliste verwendet wird, wählen wir daraus
            if use_wordlist:
                import random as _random

                if args.unique:
                    # Einmalige Auswahl ohne Ersatz
                    remaining = total - written
                    selected = _random.sample(words, remaining)
                    for pw in selected:
                        f.write(pw + '\n')
                        written += 1
                        if args.progress and written % args.progress == 0:
                            elapsed = round(time() - start, 2)
                            print(f"{written}/{total} geschrieben — {elapsed}s", end='\r', flush=True)
                else:
                    while written < total:
                        pw = secrets.choice(words)

                        if seen is not None:
                            if pw in seen:
                                continue
                            seen.add(pw)

                        f.write(pw + '\n')
                        written += 1

                        if args.progress and written % args.progress == 0:
                            elapsed = round(time() - start, 2)
                            print(f"{written}/{total} geschrieben — {elapsed}s", end='\r', flush=True)

            else:
                while written < total:
                    pw = ''.join(secrets.choice(charset) for _ in range(args.length))

                    if seen is not None:
                        if pw in seen:
                            continue
                        seen.add(pw)

                    f.write(pw + '\n')
                    written += 1

                    if args.progress and written % args.progress == 0:
                        elapsed = round(time() - start, 2)
                        print(f"{written}/{total} geschrieben — {elapsed}s", end='\r', flush=True)

        elapsed_total = round(time() - start, 2)
        print(f"\n✅ Fertig: {written} Passwörter in '{args.output}' geschrieben in {elapsed_total}s.")

        if args.unique:
            est_mem = estimate_memory_bytes_for_set(written, args.length)
            print(f"Hinweis: Eindeutige Generierung hat etwa {format_bytes(est_mem)} RAM beansprucht (Schätzung).")

    except OSError as e:
        print(f"Fehler beim Schreiben der Datei: {e}")
        sys.exit(1)


def estimate_memory_bytes_for_set(n_items, avg_length):
    
    # Diese Formel liefert nur eine grobe Größenordnung.
    avg_str_bytes = avg_length + 1  
    per_item_overhead = 72 
    return n_items * (avg_str_bytes + per_item_overhead)


def format_bytes(n):
    # Einfaches Formatieren der Bytes-Größe
    units = ['B', 'KB', 'MB', 'GB']
    i = 0
    x = float(n)
    while x >= 1024 and i < len(units)-1:
        x /= 1024.0
        i += 1
    return f"{x:.1f} {units[i]}"


if __name__ == '__main__':
    main()