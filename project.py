import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Program do konwersji danych między formatami .xml, .json, .yml/.yaml")
    
    parser.add_argument("input_file", help="Ścieżka do pliku wejściowego (np. pathFile1.json)")
    parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego (np. pathFile2.xml)")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print("Błąd: Nieprawidłowe argumenty. Sposób użycia: project.py pathFile1.x pathFile2.y")
        sys.exit(1)

    print("--- Konwerter Danych ---")
    print(f"Plik wejściowy: {args.input_file}")
    print(f"Plik wyjściowy: {args.output_file}")
    
    if not os.path.isfile(args.input_file):
        print(f"Błąd: Plik wejściowy '{args.input_file}' nie istnieje!")
        sys.exit(1)
        
    print("Parsowanie argumentów zakończone sukcesem.")

if __name__ == "__main__":
    main()