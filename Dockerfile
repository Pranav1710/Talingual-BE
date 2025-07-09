FROM python:3.10-slim

# Set environment variable
ENV ENVIRONMENT=prod

# Install system dependencies required for Playwright and general headless operation
RUN apt-get update && apt-get install -y \
    curl wget gnupg unzip \
    libgtk-3-0 libxss1 libasound2 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxtst6 libgbm1 libxrandr2 libu2f-udev libvulkan1 \
    fonts-liberation libappindicator3-1 libsecret-1-0 libgdk-pixbuf2.0-0 \
    libenchant-2-2 libgles2 libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install playwright

# Install Playwright browsers (Chromium, Firefox, WebKit)
RUN playwright install --with-deps

# Expose the port your app runs on
EXPOSE 10000

# Start the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "--workers", "1", "app:app"]
