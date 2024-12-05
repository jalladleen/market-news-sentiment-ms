# Use a slim Python base image
FROM python:3.12-slim
# Set the working directory
WORKDIR /app
# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire application
COPY . ./
# Set the frontend path for deployment
ENV FRONTEND_PATH=/app/frontend
# Expose the application port
EXPOSE 8000
# Command to run the application
CMD ["uvicorn", "src.app.main:app", "--host", "localhost", "--port", "8000"]
