This is Carlos Coll Huerta's TKS technical test.

Within the Makefile you can handle the entire flow to get everything up & running:

Install make on your computer, if you do not already have it.
Build the Docker image: make build
Migrate any DB pending task: make migrate
Start the application: make up
As you could see on the Makefile script, you could just avoid those steps and just execute make up, as build and migrate are dependants of it.

Go to http://127.0.0.1:5050/docs to see the documentation.