FROM python:3.9-slim

# Install dependencies
RUN apt-get clean && apt-get -y update && apt-get -y install nginx python3-dev build-essential nfs-common && rm -rf /var/lib/apt/lists/*

# Create mount point for NFS
RUN mkdir -p /mnt/nfs

COPY /data/demo.db /mnt/nfs

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for the application
EXPOSE 5000

# Command to run the application
CMD ["python3", "main.py"]
