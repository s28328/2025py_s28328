# CEL PROGRAMU:
# Program generuje losową sekwencję DNA o określonej długości, umieszcza w niej imię użytkownika
# (bez wpływu na statystyki), zapisuje do pliku w formacie FASTA oraz pokazuje statystyki zawartości
# poszczególnych nukleotydów (A, C, G, T) i udział par CG.

# Importujemy bibliotekę `random` do losowania znaków oraz pozycji w sekwencji.
import random

# Funkcja generująca losową sekwencję DNA o podanej długości.
def generate_dna_sequence(length):
    # Używamy generatora listy i `random.choice`, aby wybrać `length` razy losowy znak spośród A, C, G, T.
    return ''.join(random.choice('ACGT') for _ in range(length))

# Funkcja wstawiająca imię użytkownika w losowe miejsce w sekwencji DNA.
def insert_name_into_sequence(sequence, name):
    # ORIGINAL:
    # insert_pos = random.randint(0, len(sequence))
    # MODIFIED (dodano seed aby umożliwić powtarzalność dla testów/debugowania):
    # Tworzymy generator liczb pseudolosowych z ustalonym ziarnem (seed=42) dla powtarzalnych wyników.
    insert_pos = random.Random(42).randint(0, len(sequence))
    # Wstawiamy imię do sekwencji – dzielimy oryginalną sekwencję na dwie części i dodajemy imię pomiędzy.
    return sequence[:insert_pos] + name + sequence[insert_pos:]

# Funkcja obliczająca statystyki zawartości poszczególnych nukleotydów w sekwencji DNA.
def calculate_nucleotide_stats(sequence):
    # Obliczamy długość sekwencji.
    length = len(sequence)
    # Liczymy liczbę wystąpień każdego nukleotydu w sekwencji.
    count_A = sequence.count('A')
    count_C = sequence.count('C')
    count_G = sequence.count('G')
    count_T = sequence.count('T')

    # Obliczamy procentowy udział każdego nukleotydu w sekwencji.
    percent_A = 100 * count_A / length
    percent_C = 100 * count_C / length
    percent_G = 100 * count_G / length
    percent_T = 100 * count_T / length
    # Sumujemy procenty C i G jako %CG.
    percent_CG = percent_C + percent_G

    # Zwracamy wszystkie dane w formie słownika (klucz-wartość).
    return {
        'A': percent_A,
        'C': percent_C,
        'G': percent_G,
        'T': percent_T,
        'CG': percent_CG
    }

# Funkcja zapisująca sekwencję DNA do pliku FASTA z odpowiednim formatowaniem.
def save_fasta_file(filename, seq_id, description, sequence_with_name):
    # Otwieramy plik do zapisu w trybie tekstowym.
    with open(filename, 'w') as file:
        # Zapisujemy nagłówek FASTA z ID i opisem.
        file.write(f">{seq_id} {description}\n")
        # ORIGINAL:
        # file.write(sequence_with_name + "\n")
        # MODIFIED (formatowanie FASTA: linie po 60 znaków):
        # Zapisujemy sekwencję w liniach po 60 znaków – standard w plikach FASTA.
        for i in range(0, len(sequence_with_name), 60):
            # Dzielimy sekwencję na fragmenty po 60 znaków i zapisujemy każdy w osobnej linii.
            file.write(sequence_with_name[i:i+60] + "\n")

# Funkcja pomocnicza służąca do pobrania liczby całkowitej z walidacją (czy użytkownik nie wpisuje tekstu).
def get_valid_int(prompt):
    # Pętla działa, dopóki użytkownik nie poda poprawnej liczby całkowitej.
    while True:
        try:
            # Pobieramy dane i próbujemy przekonwertować je na int.
            return int(input(prompt))
        except ValueError:
            # Jeśli wystąpi błąd konwersji (np. użytkownik wpisze tekst), informujemy go o tym.
            print("Błąd: Wprowadź liczbę całkowitą.")

# Główna funkcja programu – steruje całością logiki aplikacji.
def main():
    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # MODIFIED (dodano walidację wejścia, aby uniknąć błędów przy wpisaniu tekstu zamiast liczby):
    # Pobieramy od użytkownika długość sekwencji z zabezpieczeniem przed błędnym typem danych.
    length = get_valid_int("Podaj długość sekwencji: ")

    # Pobieramy ID sekwencji od użytkownika (np. A123).
    seq_id = input("Podaj ID sekwencji: ")
    # Pobieramy opis sekwencji, np. "Losowa sekwencja testowa".
    description = input("Podaj opis sekwencji: ")
    # Pobieramy imię użytkownika, które zostanie wstawione do sekwencji.
    user_name = input("Podaj imię: ")

    # Generujemy losową sekwencję DNA o zadanej długości.
    dna_sequence = generate_dna_sequence(length)
    # Wstawiamy imię użytkownika w losowe miejsce w sekwencji (nie wpływa na statystyki).
    sequence_with_name = insert_name_into_sequence(dna_sequence, user_name)
    # Obliczamy statystyki dla sekwencji bez imienia (oryginalna sekwencja).
    stats = calculate_nucleotide_stats(dna_sequence)

    # Przygotowujemy nazwę pliku FASTA na podstawie ID sekwencji.
    filename = f"{seq_id}.fasta"
    # Zapisujemy sekwencję wraz z imieniem do pliku w formacie FASTA.
    save_fasta_file(filename, seq_id, description, sequence_with_name)

    # Wyświetlamy potwierdzenie zapisania pliku oraz statystyki nukleotydów.
    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    # Wyświetlamy procentowy udział każdego nukleotydu z zaokrągleniem do 1 miejsca po przecinku.
    print(f"A: {stats['A']:.1f}%")
    print(f"C: {stats['C']:.1f}%")
    print(f"G: {stats['G']:.1f}%")
    print(f"T: {stats['T']:.1f}%")
    # Wyświetlamy udział par CG jako sumę procentów C i G.
    print(f"%CG: {stats['CG']:.1f}")

# Sprawdzamy, czy skrypt jest uruchamiany bezpośrednio, a nie importowany jako moduł.
if __name__ == "__main__":
    # Jeśli tak – uruchamiamy główną funkcję programu.
    main()
