FROM node:14
WORKDIR /app
COPY ./package.json .
RUN npm i -g gulp
RUN npm install
COPY ./gulpfile.js .
CMD gulp
