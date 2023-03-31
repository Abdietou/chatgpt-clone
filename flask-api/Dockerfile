# Base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY . .

EXPOSE 5001

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]