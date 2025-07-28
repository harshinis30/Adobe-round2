# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install pip packages (torch pinned to CPU version)
RUN pip install --upgrade pip && \
    pip install torch==2.2.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy the local sentence-transformer model folder
COPY e5-small-v2-local/ ./e5-small-v2-local/

# Copy the rest of the application
COPY . .

# Run the application (no internet needed at this point)
CMD ["python", "main.py", \
    "--pdf_folder", "Challenge_1b/Collection 1/PDFs", \
    "--input_json", "Challenge_1b/Collection 1/challenge1b_input.json", \
    "--output", "output.json"]
