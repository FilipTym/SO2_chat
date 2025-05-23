# Systemy Operacyjne 2 – Projekt 1

**Autor:** Filip Tymiński  
**Data:** Marzec 2025

## 📌 Temat projektu

Projekt polega na stworzeniu prostego systemu komunikacji klient–serwer w języku Python z użyciem gniazd TCP, wielowątkowości oraz graficznego interfejsu użytkownika (`tkinter`). System pozwala wielu użytkownikom rozmawiać w czasie rzeczywistym przez lokalną sieć.

## 💡 Opis działania

### Serwer (`server.py`)

- Nasłuchuje na adresie `127.0.0.1:8084`.
- Obsługuje wielu klientów równocześnie (każdy w osobnym wątku).
- Rejestruje pseudonimy użytkowników.
- Wysyła wiadomości od jednego klienta do wszystkich pozostałych (broadcast).
- Obsługuje komendę `/quit` do wylogowania klienta.

### Klient (`klient.py`)

- Graficzny interfejs oparty na `tkinter`:
  - okno czatu (zielony tekst na czarnym tle),
  - pole do wpisywania wiadomości,
  - obsługa przycisku Enter.
- Łączy się z serwerem i wysyła swój pseudonim.
- Odbiera i wyświetla wiadomości w czasie rzeczywistym.
- Komenda `/quit` zamyka aplikację.

## 🧱 Kluczowe elementy techniczne

- **Wątki** (`threading`): obsługa wielu klientów na serwerze oraz odbieranie wiadomości w tle u klienta.
- **Gniazda TCP** (`socket`): komunikacja klient–serwer.
- **Synchronizacja** (`Lock`): bezpieczna modyfikacja listy aktywnych klientów.
- **GUI** (`tkinter`): prosty, terminalowy interfejs graficzny klienta.

## ⚠️ Napotkane problemy i rozwiązania

- **Rozłączenia klientów**: serwer obsługuje sytuacje, gdy klient zamknie aplikację bez wysłania `/quit`.
- **Błąd warunku uruchamiania**: poprawiono `if _name_ == "_main_"` → `if __name__ == "__main__":`.
- **Bezpieczeństwo GUI**: aktualizacja interfejsu wykonywana wyłącznie przez główny wątek.

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
