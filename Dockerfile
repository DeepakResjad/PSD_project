# Use an official Python image as the base
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port your app runs on (adjust as needed)
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
