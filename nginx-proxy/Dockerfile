FROM nginx:alpine

RUN apk add --no-cache certbot certbot-nginx

COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY nginx/conf.d/ /etc/nginx/conf.d/

RUN mkdir -p /etc/nginx/ssl

EXPOSE 80 443