FROM continuumio/miniconda3

WORKDIR /src/app

# Create environment
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "ml-paper-topic-modelling", "/bin/bash", "-c"]

RUN apt-get install -y gunicorn

COPY src/app/ .
RUN chmod +X gunicorn.sh
ENTRYPOINT ["bash", "gunicorn.sh"]