FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y ffmpeg cron

# Setup source scripts and the environment
WORKDIR /app
ADD *.py ./
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Setup cron jobs
ADD cron_jobs .
RUN chmod 0644 cron_jobs
RUN crontab cron_jobs
RUN touch /var/log/cron.log

# Run cron jobs and push logs to the stdout. This is useful when debugging
CMD cron && tail -f /var/log/cron.log
