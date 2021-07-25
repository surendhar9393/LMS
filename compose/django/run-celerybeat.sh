#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m celeryuser -c "celery -A LMS beat -l INFO --pidfile="
