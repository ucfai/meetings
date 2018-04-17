FROM %%base%%

ENV PATH /notebooks/__admin__:$PATH

RUN apt-get update

RUN apt-get install -y bzip2 wget                 

## Conda
RUN    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-%%conda%%-Linux-x86_64.sh \
    && /bin/bash Miniconda3-%%conda%%-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-%%conda%%-Linux-x86_64.sh
ENV PATH /opt/conda/bin:$PATH

ADD env/%%type%%.yml /%%type%%.yml
RUN conda env create -f /%%type%%.yml

ENV PATH /opt/conda/envs/%%name%%/bin:$PATH

## Cleaning up
RUN apt-get clean  \
&& rm -rf /var/lib/apt/lists/*  \
&& conda clean --tarballs -y  \
&& conda clean --packages -y

WORKDIR "/%%name%%"
EXPOSE 8888

CMD ["jupyter", "notebook"]