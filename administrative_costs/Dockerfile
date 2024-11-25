FROM ubuntu:latest

# Ustawienie katalogu roboczego
WORKDIR /app

# Zainstaluj zależności
# Zainstaluj wymagane pakiety, w tym Python oraz pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    locales \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libasound2t64 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    && locale-gen pl_PL.UTF-8 \
    && update-locale LANG=pl_PL.UTF-8 \
    && rm -rf /var/lib/apt/lists/*



# Skopiuj pliki projektu do katalogu roboczego
WORKDIR /app
COPY . /app


# Utwórz i aktywuj środowisko virtualne
RUN python3 -m venv .venv

# Aktywuj i zainstaluj zależności
RUN . .venv/bin/activate && pip install -r requirements.txt
RUN /app/.venv/bin/python -m playwright install

# Kopiowanie pliku konfiguracyjnego Streamlit
COPY .streamlit/config.toml /root/.streamlit/config.toml
ENV STREAMLIT_SERVER_ENABLECORS="true"
ENV STREAMLIT_SERVER_ALLOWORIGIN="http://localhost:8000"


# Nadaj uprawnienia do wykonania skryptu start.sh
RUN chmod +x /app/start.sh

# Aktywacja środowiska i uruchomienie aplikacji
ENTRYPOINT ["/bin/bash", "-c", ". .venv/bin/activate && exec \"$@\"", "--"]


#CMD ["streamlit", "run", "/app/reports/main.py", "--server.address=0.0.0.0"]
CMD ["/app/start.sh"]

