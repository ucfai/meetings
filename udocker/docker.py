import os
from subprocess import call, check_output

import utils

## possible base images for the Dockerfiles
_base = {
	"cpu": "library/ubuntu:16.04",
	"gpu": "nvidia/cuda:9.1-base-ubuntu16.04",
}


## accepted Dockerfiles
accepted = ["udocker/{}.Dockerfile".format(f) for f in _base.keys()]
template =  "udocker/template.Dockerfile"


################################################################################
## Docker tagging and arguments
################################################################################

## docker image construction, host/image:tag
hst = "ucfsigai"
img = "intelligence"
tag = None  ## should be unset, is based on user spec'd args
container = None

## build arguments
conda = "4.4.10"

## runtime arguments
PORT = 19972
args_start = []


def _container(use_gpu):
	global tag
	tag = "gpu" if use_gpu else "cpu"
	tag = "{}-{}".format(get_sem(), tag)

	global container
	container = "{}/{}:{}".format(hst, img, tag)

	global args_start
	args_start = []
	args_start.append("-v $(pwd):/{}".format(img))					## mount nanodegree
	args_start.append("-v $(pwd)/udocker/.jupyter:/root/.jupyter")	## mount custom jupyter configs
	args_start.append("-p {}:8888".format(PORT))					## jupyter->localhost port



def start(use_gpu, attach=True):
	_container(use_gpu)

	## stop current running container
	if check_output("docker inspect -f {{.State.Running}} {}".format(img), shell=True).strip().decode("utf-8") == "true":
		call("docker stop {}".format(img))


	args_default = [
		"--runtime=nvidia" if use_gpu else "", 	## runtime
		"--rm", 								## remove on stop
		"-d" if not attach else "",				## run container in detached _mode
		"--name {}".format(img), 				## name container for simpler management
	]

	return call(" ".join(
		["docker", "run"]
		+ args_default
		+ args_start
		+ [container]
	), shell=True)


def pull(use_gpu):
	_container(use_gpu)

	return call("docker pull {}".format(container), shell=True) == 0


def build(use_gpu):
	dockerfile = "udocker/{}.Dockerfile".format(tag)
	assert dockerfile in accepted

	args_default = [
		"-t {}".format(container),	## tag the container
		"-f {}".format(dockerfile),	## dockerfile
	]

	if dockerfile not in os.listdir(os.getcwd()):
		with open(template, "r") as tmpl, open(dockerfile, "w") as outp:
			read = tmpl.read()
			read = read.replace("%%base%%", _base[tag])
			read = read.replace("%%conda%%", conda)
			read = read.replace("%%type%%", tag)
			read = read.replace("%%name%%", img)
			outp.write(read)

	return call(" ".join(
		["docker", "build"]
		+ args_default
		+ ["udocker"]
	), shell=True)

