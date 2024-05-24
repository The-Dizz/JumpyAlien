# Use an official Python runtime as a parent image
FROM python:2.7

# Install necessary system dependencies for Pygame and display management
RUN apt-get update && apt-get install -y \
    libsdl-dev \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libfreetype6-dev \
    x11-apps \
    x11-xserver-utils \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Pygame 1.9.4
RUN pip install pygame==1.9.4

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set the entrypoint to xvfb-run to simulate a display
ENTRYPOINT ["xvfb-run", "-s", "-screen 0 640x480x24", "python", "main.py"]

