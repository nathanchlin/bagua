FROM python:3.9-slim

WORKDIR /app

# 设置pip源为清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5005

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PORT=5005

CMD ["python", "app.py"] 