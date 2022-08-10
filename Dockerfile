ARG timeZone=Europe/Kaliningrad
FROM python:3.10.5-slim-bullseye as runner
WORKDIR /app
COPY . .
#setcap cap_net_raw+ep $(readlink -f $(which python3)); \
RUN set -eux; \
    apt update; \
    apt install -y --no-install-recommends tzdata; \ 
    pip3 install -r requirements.txt; 
ENV TZ=${timeZone}
CMD ["python", "app.py"]