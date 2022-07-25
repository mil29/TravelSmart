#!/bin/bash
sed -i '14 i \tclient_max_body_size 100M;' /etc/nginx/nginx.conf
service nginx restart