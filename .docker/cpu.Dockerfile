## Nvidia Drives Repo:
## - http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/

## TensorFlow's GPU image is based on Ubuntu 16.04 LTS
## It's also built here: https://github.com/tensorflow/tensorflow/blob/b43d0f3c98140edfebb8295ea4a4b661e2fc2a85/tensorflow/tools/docker/Dockerfile.gpu
FROM tensorflow/tensorflow:1.4.1-py3

## Setup the project directory bin
ENV PATH /notebooks/__admin__:$PATH
# ENV ADMIN /notebooks/__admin__

## Install some extra, left-out, packages
RUN pip install \
      colorlover==0.2.1                    \
      jupyter_contrib_nbextensions==0.3.3  \
      nbconvert==5.3.1                     \
      plotly==2.2.0                        \
      pyyaml==3.12                         \
      RISE==5.1.0                          \
      seaborn==0.8.0                       \
      tables==3.4.2                      ; \
    pip install jupyter-c-kernel==1.2.2 && install_c_kernel

## Configure RISE from `pip`
RUN    jupyter nbextension install rise --py --sys-prefix \
    && jupyter nbextension enable  rise --py --sys-prefix \
    && jupyter contrib nbextension install \
    && jupyter nbextension enable codefolding/main \
    && jupyter nbextension enable execute_time/ExecuteTime \
    && jupyter nbextension enable hide_input/main \
    && jupyter nbextension enable python-markdown/main \
    && jupyter nbextension enable toggle_all_line_numbers/main \
    && jupyter nbextension enable hide_input_all/main \
    && jupyter nbextension enable splitcell/splitcell \
    && jupyter nbextension enable exercise2/main \
    && jupyter nbextension enable code_prettify/code_prettify \
    && jupyter nbextension enable equation-numbering/main \
    && jupyter nbextension enable highlighter/highlighter \
    && jupyter nbextension enable table_beautifier/main

RUN    apt-get -y update \
    && apt-get -y install \
        build-essential \
        curl \
        make \
        gcc \
        git \
        perl \
    && git clone https://github.com/pjreddie/darknet.git /darknet \
    && (   cd /darknet \
        && make \
        && mv include/* src/ \
        && rm -rf include .git) \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*


## Big brother, but for SASS
# sass --watch /root/.jupyter/custom/sass/:/root/.jupyter/custom/

CMD ["jupyter", "notebook"]
