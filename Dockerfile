FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# BUILDING FLASK IMAGE: docker build -t flask-smorest-sql-api .  
# RUNNING FLASK IMAGE WITH HOT RELOAD: docker run -d -p 5000:5000 -w /app -v "${PWD}:/app" flask-smorest-sql-api
# RUNNING NORMAL IMAGE FOR RELEASE: docker run -d -p 5000:5000 flask-smorest-sql-api