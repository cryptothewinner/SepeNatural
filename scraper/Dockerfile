FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests beautifulsoup4

# Copy the script
COPY main.py .

# Run the scraper
CMD ["python", "main.py"]
