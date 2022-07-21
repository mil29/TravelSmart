#!/bin/bash
# source "$PYTHONPATH/activate" && {
# # log which migrations have already been applied
# python manage.py showmigrations;
# # migrate
# python manage.py migrate --noinput;
# }
# if [[ $EB_IS_COMMAND_LEADER == "true" ]];
# then   python manage.py migrate --noinput;  
# python manage.py collectstatic --noinput;
# else   echo "this instance is NOT the leader";
# fi...