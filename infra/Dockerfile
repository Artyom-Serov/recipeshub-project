FROM nginx:1.22.1
#COPY ./infra/nginx.conf /etc/nginx/nginx.conf
COPY ./infra/nginx.conf /etc/nginx/templates/default.conf.template
#COPY nginx.conf /etc/nginx/templates/default.conf.template

#WORKDIR /usr/src/app
#
#EXPOSE 80
#EXPOSE 443
#
#CMD ["nginx", "-g", "daemon off;"]