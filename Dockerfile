FROM python:3.10.6

WORKDIR /

RUN pip install "poetry==1.3.1"



COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL: $DATABASE_URL
ENV SECRET_KEY: $SECRET_KEY


COPY . .

EXPOSE 8000
ENTRYPOINT ["bash","entrypoint.sh"]
CMD ["gunicorn", "TodoList_App.wsgi", "-w", "4","-b","0.0.0.0:8000"]




