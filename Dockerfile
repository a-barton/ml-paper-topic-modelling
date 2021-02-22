FROM continuumio/miniconda3

WORKDIR /src/app

# Create environment
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "ml-paper-topic-modelling", "/bin/bash", "-c"]

# Make sure environment is activated
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

COPY src/app/ .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ml-paper-topic-modelling", "python", "app.py"]