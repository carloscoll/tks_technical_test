This is Carlos Coll Huerta's TKS technical test.

Within the Makefile you can handle the entire flow to get everything up & running:

1. Install make on your computer, if you do not already have it.
2. Build the Docker image: make build
3. Migrate any DB pending task: make migrate
4. Start the application: make up
5. 
As you could see on the Makefile script, you could just avoid those steps and just execute make up, as build and migrate are dependants of it.

Go to http://127.0.0.1:5050/docs to see the documentation.