FROM continuumio/miniconda3:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5900
CMD python ./lyrics_analyzer.py
