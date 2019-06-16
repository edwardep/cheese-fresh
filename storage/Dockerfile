FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt
COPY . /app
ARG STORAGE_ID
ENV STORAGE_ID ${STORAGE_ID}
CMD flask run --host 0.0.0.0 --port 100${STORAGE_ID}