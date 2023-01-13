FROM node:19-alpine

WORKDIR /view
ENV PATH /view/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm install
RUN npm install -g @vue/cli

CMD ["npm", "run", "serve"]