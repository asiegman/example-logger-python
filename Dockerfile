FROM python:3-slim

# Set this to anything else to have a single run with example log messages
ENV LOOP_FOREVER true

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY app.py /app.py

ENTRYPOINT ["python"]

CMD ["app.py"]
