FROM node:22.4.0-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

# RUN npm ci --only=production

COPY . .

