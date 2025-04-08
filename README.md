# Production Manager App 📊

Aplikacja do zarządzania produkcją i monitorowania zleceń. Wykorzystuje bazę danych **PostgreSQL** hostowaną na **Render** oraz aplikację frontendową stworzoną za pomocą **Streamlit**.

---

## 📌 Funkcje

- 🔑 **Logowanie użytkowników** (Admin/Operator).
- ➕ **Dodawanie nowych zleceń produkcyjnych** za pomocą formularza.
- 📊 **Przeglądanie i analizowanie danych produkcyjnych**.
- 💾 **Zapisywanie danych do PostgreSQL na Render**.
- 📈 **Generowanie raportów i wykresów** (w przyszłości).
- 📂 **Automatyczne backupy** (planowane).
- 📂 **Zarządzanie użytkownikami** (dodawanie, edytowanie, usuwanie).

---

## 🔨 Instalacja

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/ChinQuan/ProductionManagerApp.git
cd ProductionManagerApp

## 2.Odpalanie programu.
streamlit run app.py
