# build the Vue application
FROM node:16-alpine AS dist
WORKDIR /opt/project
COPY ./ ./
RUN npm i
ENV NODE_ENV=production

RUN npm run build

# build the nginx image
FROM nginx:1.17
COPY --from=dist /opt/project/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
