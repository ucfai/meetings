FROM phusion/baseimage:0.9.22

CMD ["/sbin/my_init"]

ENTRYPOINT ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y \
        bzip2 \
        git \
        net-tools \
        unzip \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
    && wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh \
    && /bin/bash Miniconda3-4.3.21-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-4.3.21-Linux-x86_64.sh

ENV PATH /opt/conda/bin:$PATH
ADD environment.yml /environment.yml
RUN conda install conda=4.3.21 -y \
    && conda env create -f /environment.yml \
    && conda clean --tarballs -y \
    && conda clean --packages -y

RUN mkdir -p /srv/sigai
WORKDIR /srv/sigai

EXPOSE 8888
EXPOSE 8000

ENV PATH /opt/conda/envs/sigai_meetings/bin:$PATH
CMD ["jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token="]
