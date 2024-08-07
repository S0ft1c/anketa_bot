# Use the latest Python image as the base
FROM python:latest

# Set the working directory
WORKDIR /bot

# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Define the command to run when the container starts
CMD ["python3", "main.py"]
