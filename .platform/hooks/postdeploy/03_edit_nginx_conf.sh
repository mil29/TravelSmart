#!/bin/bash
cat /etc/nginx/nginx.conf
sudo sed -i '14 i \t client_max_body_size 100M;' /etc/nginx/nginx.conf
sudo service nginx restart