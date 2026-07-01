import argparse
import sys
import os
import json
import yaml

def load_data(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.json':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("Pomyślnie wczytano plik JSON.")
            return data
        except json.JSONDecodeError as e:
            print(f"Błąd: Niepoprawna składnia pliku JSON w {file_path}. Szczegóły: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku: {e}")
            sys.exit(1)
            
    elif ext in ['.yml', '.yaml']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            print("Pomyślnie wczytano plik YAML.")
            return data
        except yaml.YAMLError as e:
            print(f"Błąd: Niepoprawna składnia pliku YAML w {file_path}. Szczegóły: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku: {e}")
            sys.exit(1)
            
    else:
        print(f"Błąd: Format {ext} nie jest jeszcze obsługiwany przy wczytywaniu.")
        sys.exit(1)

def save_data(data, file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.json':
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Pomyślnie zapisano dane do pliku: {file_path}")
        except Exception as e:
            print(f"Błąd podczas zapisu do pliku: {e}")
            sys.exit(1)
            
    elif ext in ['.yml', '.yaml']:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print(f"Pomyślnie zapisano dane do pliku: {file_path}")
        except Exception as e:
            print(f"Błąd podczas zapisu do pliku: {e}")
            sys.exit(1)
            
    else:
        print(f"Błąd: Format {ext} nie jest jeszcze obsługiwany przy zapisie.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Program do konwersji danych między formatami .xml, .json, .yml/.yaml")
    parser.add_argument("input_file", help="Ścieżka do pliku wejściowego")
    parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print("Błąd: Nieprawidłowe argumenty. Sposób użycia: project.py pathFile1.x pathFile2.y")
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Błąd: Plik wejściowy '{args.input_file}' nie istnieje!")
        sys.exit(1)
        
    # Wczytywanie danych z pliku wejściowego
    data = load_data(args.input_file)
    
    # Zapisywanie danych do pliku wyjściowego
    save_data(data, args.output_file)

if __name__ == "__main__":
    main()