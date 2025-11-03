FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
COPY next.config.ts ./
COPY tsconfig.json ./

RUN npm install

COPY . .

RUN npx next build

EXPOSE 3000

CMD ["npm", "start"]