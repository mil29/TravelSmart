#!/bin/bash
# this command adds 'client_max_body_size variable to nginx.conf file so that profile_pic upload won't give nginx 403 error , this needs to be added on every deploy as elastic beanstalk resets the conf file
sudo sed -i '14 i \    client_max_body_size 100M;' /etc/nginx/nginx.conf
sudo service nginx restart