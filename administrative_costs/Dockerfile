FROM ubuntu:latest

# Ustawienie katalogu roboczego
WORKDIR /app

# Zainstaluj zależności
# Zainstaluj wymagane pakiety, w tym Python oraz pip
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Skopiuj pliki projektu do katalogu roboczego
WORKDIR /app
COPY . /app


# Utwórz i aktywuj środowisko virtualne
RUN python3 -m venv .venv

# Aktywuj i zainstaluj zależności
RUN . .venv/bin/activate && pip install -r requirements.txt

# Aktywacja środowiska i uruchomienie aplikacji
ENTRYPOINT ["/bin/bash", "-c", ". .venv/bin/activate && exec \"$@\"", "--"]
CMD ["streamlit", "run", "/app/reports/main.py", "--server.address=0.0.0.0"]
