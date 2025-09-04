FROM node AS build

WORKDIR /app

COPY ./myapp/package.json .
COPY ./myapp/package-lock.json .
RUN npm install
COPY ./myapp .
RUN npm run build

FROM python:3.13

# установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# настройка прав
RUN useradd -m user
USER user
WORKDIR /home/user

COPY --from=build /app/build /home/user/static

# копирование самого проекта
COPY . .

CMD [ "python", "-u", "main.py" ]
