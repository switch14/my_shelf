FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

#作業ディレクトリ
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#ローカルのプロジェクトをDocker側にコピー
COPY . .

#起動コマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

