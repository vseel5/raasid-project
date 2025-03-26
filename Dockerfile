# Use a lightweight official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your project folder into the container
COPY . .

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && apt-get remove -y gcc build-essential \
 && apt-get autoremove -y \
 && apt-get clean


# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


