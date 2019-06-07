FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt
COPY . /app
RUN mkdir media1000
EXPOSE 1000
CMD ["flask","run","--host","0.0.0.0","--port","1000"]