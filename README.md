# Systemy Operacyjne 2 – Projekt 1

**Autorzy:** Filip Tymiński i Miłosz Halicki  
**Data:** Maj 2025

## 📌 Temat projektu

Projekt polega na stworzeniu prostego, wielowątkowego systemu komunikacji klient–serwer w języku Python. System umożliwia rozmowę wielu użytkowników w czasie rzeczywistym przy użyciu lokalnej sieci i podstawowych mechanizmów synchronizacji.

## 🧠 Opis problemu

Z punktu widzenia systemów operacyjnych projekt demonstruje klasyczne zagadnienia:

- **Komunikacja międzyprocesowa (IPC)** — dzięki gniazdom TCP,
- **Wielowątkowość i równoległość** — obsługa wielu klientów jednocześnie,
- **Sekcje krytyczne i synchronizacja** — ochrona współdzielonych zasobów,
- **Zamykanie połączeń i obsługa wyjątków** — niezawodność komunikacji.

Projekt pokazuje, jak przy użyciu prostych narzędzi zaimplementować model klient–serwer, który musi być odporny na błędy, bezpieczny i wydajny.

## 🔁 Struktura wątków

### Wątki na serwerze

- **Główny wątek serwera:** nasłuchuje połączeń na porcie.
- **Wątki klientów:** każdy klient obsługiwany jest w osobnym wątku (`threading.Thread`), co umożliwia równoległe przetwarzanie wiadomości.

### Wątki po stronie klienta

- **Wątek GUI (główny wątek Tkintera):** obsługuje interfejs użytkownika.
- **Wątek odbierania wiadomości:** działa w tle, słucha wiadomości przychodzących z serwera.

## 🔐 Sekcje krytyczne i synchronizacja

### Sekcje krytyczne

- **Słownik klientów `clients`** na serwerze: wspólna struktura danych modyfikowana przez wiele wątków.
- **Interfejs GUI** klienta: `tkinter` nie jest bezpieczny wątkowo — wszystkie operacje GUI muszą być wykonywane w głównym wątku.

### Zastosowane rozwiązania

- **Blokada (`threading.Lock`)** zabezpiecza dostęp do listy klientów na serwerze.
- **Brak bezpośredniego dostępu do GUI z innych wątków:** komunikaty są przekazywane poprzez odpowiednie metody aktualizujące interfejs tylko w głównym wątku.

## 💡 Funkcjonalność

- Rejestracja pseudonimu po połączeniu.
- Wysyłanie i odbieranie wiadomości w czasie rzeczywistym.
- Informacja o dołączeniu/opuszczeniu czatu przez innych użytkowników.
- Komenda `/quit` umożliwia bezpieczne opuszczenie aplikacji.

## ▶️ Uruchamianie

### 1. Serwer:
```bash
python server.py
```
### 1. Klient:
```bash
python klient.py
```

## 🧪 Przykład działania
1. Uruchom serwer (server.py).
2. Uruchom klienta (klient.py) – możesz uruchomić kilka instancji w różnych terminalach lub na różnych komputerach.
3. Podaj pseudonimy i rozpocznij rozmowę.
4. Aby opuścić czat, wpisz /quit.

## Projekt wykonany w ramach przedmiotu "Systemy Operacyjne 2" na kierunku Informatyka.
