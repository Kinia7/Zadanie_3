import os
import shutil
import sys
import concurrent.futures

def normalize(name):
    # Transliteracja polskich liter na znaki ASCII
    normalized_name = name.encode('ascii', 'ignore').decode('utf-8')

    # Zamiana wszystkich liter, oprócz znaków i cyfr, na '_'
    normalized_name = ''.join(c if c.isalnum() or c in ('_', '.') else '_' for c in normalized_name)

    return normalized_name

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        # Ignoruj pewne foldery
        dirs[:] = [d for d in dirs if d.lower() not in ('archives', 'video', 'audio', 'documents', 'images')]

        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

def process_file(file_path):
    # Pobierz rozszerzenie pliku
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension[1:].upper()  # Usuń kropkę i zamień na wielkie litery

    # Normalizuj nazwę pliku
    normalized_name = normalize(os.path.basename(file_path))
    
    # Kategorie plików
    categories = {
        'JPEG': 'images',
        'PNG': 'images',
        'JPG': 'images',
        'SVG': 'images',
        'AVI': 'video',
        'MP4': 'video',
        'MOV': 'video',
        'MKV': 'video',
        'DOC': 'documents',
        'DOCX': 'documents',
        'TXT': 'documents',
        'PDF': 'documents',
        'XLSX': 'documents',
        'PPTX': 'documents',
        'MP3': 'audio',
        'OGG': 'audio',
        'WAV': 'audio',
        'AMR': 'audio',
        'ZIP': 'archives',
        'GZ': 'archives',
        'TAR': 'archives'
    }

    # Sprawdź kategorię pliku
    if file_extension in categories:
        category_folder = categories[file_extension]
        category_path = os.path.join(os.path.dirname(file_path), category_folder)

        # Jeśli to archiwum, wypakuj zawartość do odpowiedniego podfolderu
        if category_folder == 'archives':
            archive_folder_path = os.path.join(category_path, normalized_name)
            os.makedirs(archive_folder_path, exist_ok=True)
            shutil.unpack_archive(file_path, archive_folder_path)
        else:
            # Przenieś plik do odpowiedniego folderu
            os.makedirs(category_path, exist_ok=True)
            shutil.move(file_path, os.path.join(category_path, normalized_name))
    else:
        # Jeśli nieznane rozszerzenie, pozostaw plik bez zmiany
        pass

def main():
    # Sprawdzenie poprawności liczby argumentów
    if len(sys.argv) != 2:
        print("Użycie: python balagan.py <ścieżka_do_folderu>")
        sys.exit(1)

    # Pobranie ścieżki folderu z argumentu
    folder_path = sys.argv[1]

    # Sprawdzenie istnienia podanej ścieżki
    if not os.path.exists(folder_path):
        print("Podana ścieżka nie istnieje.")
        sys.exit(1)

    # Utworzenie puli wątków
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Uruchomienie przetwarzania folderu w osobnym wątku
        future = executor.submit(process_folder, folder_path)
        try:
            # Pobranie wyniku lub obsłużenie wyjątku
            result = future.result()
        except Exception as e:
            print(f"Błąd podczas przetwarzania folderu: {e}")

if __name__ == "__main__":
    main()
