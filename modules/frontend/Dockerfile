FROM node:14.8.0-buster

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

RUN npm install -g react-scripts@3.4.3

COPY . ./

EXPOSE 3000

CMD ["npm", "start"]