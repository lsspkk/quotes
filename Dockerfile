# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 8042 available to the world outside this container
EXPOSE 8042

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python3", "api.py"]