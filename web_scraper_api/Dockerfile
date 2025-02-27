# Start with the base image for Ubuntu 22.04
FROM python:3.13

# Set environment variables to avoid interactive prompts during package installation
ENV PYTHONUNBUFFERED=1

# Install dependencies, Chrome, locales, and other packages
RUN apt-get update -qq -y && \
    apt-get install -y \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-4-1 \
        libnss3 \
        xdg-utils \
        wget && \
    wget -q -O chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.141/linux64/chromedriver-linux64.zip && \
    unzip chrome-linux64.zip && \
    rm chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome/ && \
    ln -s /opt/chrome/chrome /usr/local/bin/ && \
    wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
    unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
    rm chromedriver-linux64.zip && \
    mv chromedriver /usr/local/bin/

# Create a non-privileged user
RUN useradd -m -d /home/nonrootuser -s /bin/bash nonrootuser

# Set working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Change ownership of the application directory to the non-privileged user
RUN chown -R nonrootuser:nonrootuser /app

# Switch to the non-privileged user
USER nonrootuser

# Command to run the backend
CMD ["python3", "main.py"]
