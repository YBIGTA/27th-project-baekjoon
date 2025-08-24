FROM python:3.12-slim

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# install boj-cli
RUN git clone https://github.com/ingbunga/boj-cli.git
RUN cd boj-cli && pip install -e '.[dev]'

COPY . .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]