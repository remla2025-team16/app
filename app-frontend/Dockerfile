FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY index.html script.js config.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
