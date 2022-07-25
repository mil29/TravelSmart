#!/bin/bash
# this command adds in client_max_body_size to prevent file overload error on profile pic upload page, into nginx.conf file as the conf file resets on every deploy through elastic beanstalk
sudo sed -i '14 i \tclient_max_body_size 100M;' /etc/nginx/nginx.conf
sudo service nginx restart