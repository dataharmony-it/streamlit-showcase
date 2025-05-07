FROM python:3.10

WORKDIR /app

COPY ./ /app/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8051

HEALTHCHECK CMD curl --fail http://localhost:8051/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8051", "--server.address=0.0.0.0"]
