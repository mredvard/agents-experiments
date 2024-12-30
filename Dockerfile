FROM continuumio/miniconda3:latest

COPY environment.yml /app/environment.yml

RUN conda env update -f /app/environment.yml

WORKDIR /app