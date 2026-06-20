# build env
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . ./
RUN npm run build
CMD ["cp", "-r", "/app/build/.", "/frontend_static/"]