FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

WORKDIR /code/backend

# RUN cd backend/

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
# No workers for single thread.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# uvicorn main:app --host 0.0.0.0 --port 11253 --workers 4