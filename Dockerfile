FROM continuumio/miniconda3

WORKDIR /opt/pp
ADD src src
ADD environment.yml environment.yml
RUN conda env create -f environment.yml

CMD ["python", "src/index.py"]