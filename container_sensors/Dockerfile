FROM python:3.7
COPY startupsensor.sh .
RUN pip install procfs-sensor
RUN pip install pydstat

CMD ["/bin/bash","-c","./startupsensor.sh"]