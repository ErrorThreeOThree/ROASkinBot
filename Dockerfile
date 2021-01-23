FROM jjanzic/docker-python3-opencv

RUN CPUCOUNT=$(nproc)

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python ROASkinBot.py