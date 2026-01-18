# Meraki Always-On Sandbox – Configuration Sync

Ten projekt służy do pobierania konfiguracji z Cisco Meraki (organizacje i urządzenia) oraz automatycznego wersjonowania zmian w repozytorium Git. Dzięki temu możesz w prosty sposób śledzić zmiany konfiguracji infrastruktury sieciowej.

---

## Wymagania

* Konto Cisco Meraki
* Utworzony **Meraki Always-On Sandbox**
* Git

---

## Konfiguracja po stronie Cisco Meraki

1. Zaloguj się do Cisco Meraki Dashboard.
2. Utwórz lub uruchom **Always-On Sandbox**.
3. Wygeneruj **API Key**:

   * Dashboard → My profile → API access
4. Zanotuj:

   * `API_KEY`
   * `BASE_URL` (adres API Meraki, np. [https://api.meraki.com/api/v1](https://api.meraki.com/api/v1))

---

## Konfiguracja lokalnego środowiska

### 1. Instalacja zależności

Zainstaluj wymagane biblioteki z pliku `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 2. Plik `.env`

W katalogu głównym projektu utwórz plik `.env` z następującą zawartością:

```env
API_KEY=twoj_api_key_z_meraki
BASE_URL=https://api.meraki.com/api/v1
```

Plik `.env` nie powinien być commitowany do repozytorium.

---

## Działanie aplikacji

Po uruchomieniu skryptu aplikacja:

1. Inicjalizuje repozytorium Git (w working directory), jeśli nie zostało wcześniej utworzone.
2. Łączy się z Cisco Meraki API przy użyciu danych z pliku `.env`.
3. Pobiera:

   * listę organizacji,
   * listę urządzeń przypisanych do każdej organizacji.
4. Zapisuje konfigurację do plików w repozytorium.
5. Sprawdza, czy nastąpiły zmiany w konfiguracji.
6. Jeśli wykryto zmiany:

   * wykonuje commit do repozytorium Git z aktualnym stanem konfiguracji.