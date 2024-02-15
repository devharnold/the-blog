# Use the official Python image as base image
FROM python:3.10

#Environment variables
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONBUFFERED 1

#working directory
WORKDIR /app

#copy dependancies file to the working directory
COPY requirements.txt .

#installation of additional dependancies
RUN pip install --no-cache-dir -r requirements.txt

#copying the rest of the app code to working dir
COPY . .

#The app runs on port 
EXPOSE 5000

CMD ["python", "app.py"]