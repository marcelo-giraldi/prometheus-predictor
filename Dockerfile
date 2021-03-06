FROM continuumio/miniconda3

WORKDIR /opt/pp
ADD src src
ADD config config
ADD environment.yml environment.yml
RUN conda env create -f environment.yml

VOLUME ["/opt/pp/config"]

CMD ["/opt/conda/envs/prophet-env/bin/python", "src/index.py"]