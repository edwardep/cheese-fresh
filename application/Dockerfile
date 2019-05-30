FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["flask","run","--host","0.0.0.0"]