#!/bin/bash
sudo sed -i '14 i \tclient_max_body_size 100M;' /etc/nginx/nginx.conf
sudo service nginx restart