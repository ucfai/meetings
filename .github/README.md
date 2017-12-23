# SIGAI Meetings

In this repo, you'll find all the SIGAI@UCF lectures and workshops, categorized by semester.

Table of Contents:
- [Insallation Instructions](#installation-instructions)
- [Dependencies](#dependencies)

## Installation Instructions
To get things up and running, all you need to have Docker and `docker-compose` installed on your machine.  **(If you don't, see [Dependencies](#dependencies).)** Once you've guaranteed that...
1. `cd meetings`
1. `docker-compose build` to get the container setup
1. `docker-compose up` to start the container
1. Open `localhost:19972` in your browser and navigate to the semester you'd like to view.


## Dependencies
- [Docker](https://www.docker.com/community-edition)
  - You need a 2011 Macbook Pro or later to run the macOS version of Docker.
  - You need Windows 10 Pro, Education, or Enterprise to run the Windows version of Docker. (More specifically, you need Hyper-V installed on your machine.)
- [`docker-compose`](https://github.com/docker/compose/)