# weather-mcp/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Expose the port FastMCP listens on (from your main.py)
EXPOSE 8001

# Run the FastMCP server
CMD ["python", "main.py"]