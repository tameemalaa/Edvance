FROM node:alpine

WORKDIR '/app'

# Copy package.json first to avoid unnecessary npm installs
COPY ./package.json ./
COPY ./package-lock.json ./

RUN npm install

COPY . .

