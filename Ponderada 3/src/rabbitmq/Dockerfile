# Dockerfile-rabbitmq-setup
FROM rabbitmq:3-management

RUN apt-get update && apt-get install -y curl \
    && curl -L -o /usr/local/bin/rabbitmqadmin https://raw.githubusercontent.com/rabbitmq/rabbitmq-management/v3.8.9/bin/rabbitmqadmin \
    && chmod +x /usr/local/bin/rabbitmqadmin

COPY setup_rabbitmq.sh /setup_rabbitmq.sh
RUN chmod +x /setup_rabbitmq.sh
