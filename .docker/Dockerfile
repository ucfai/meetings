## Nvidia Drives Repo:
## - http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/

## TensorFlow's GPU image is based on Ubuntu 16.04 LTS
## It's also built here: https://github.com/tensorflow/tensorflow/blob/b43d0f3c98140edfebb8295ea4a4b661e2fc2a85/tensorflow/tools/docker/Dockerfile.gpu
FROM tensorflow/tensorflow:1.4.1-gpu-py3

## Setup the project directory bin
ENV PATH /notebooks/bin:$PATH

## Install some extra, left-out, packages
RUN pip install \
      colorlover==0.2.1 \
      nbconvert==5.3.1  \
      plotly==2.0.11    \
      pyyaml==3.12      \
      RISE==5.1.0       \
      seaborn==0.8.0    \
      tables==3.4.2

# EXPOSE 8000

## Configure RISE from `pip`
RUN jupyter nbextension install rise --py --sys-prefix && \
    jupyter nbextension enable  rise --py --sys-prefix

CMD ["jupyter", "notebook"]
