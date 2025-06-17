truc: 
	echo "This is a Makefile example."

install :
	@echo "Installing the application..."
	pip-compile requirements.in
	pip install -r requirements.txt --quiet
	pip install -e . --quiet
	@echo "✅ Application installed successfully. "

.PHONY : train
train : install
	@echo "Training the model..."
	@echo "This may take a while, please be patient."
	@echo "Running training script..."
	python -c "from main import train; train()"
	@echo "✅ Model trained successfully."

.PHONY : tests
tests :
	@echo "Running tests..."


###################################################

# Web

run_api:
	@echo "Starting the FastAPI application..."
	uvicorn api.webapi:api --host 0.0.0.0 --port 8000 --reload

test_api:
	@echo "Running API tests..."
	curl -X 'GET' 'http://127.0.0.1:8000/' \
		 -H 'accept: application/json'


###################################################

# Docker
docker_build:
	@echo "Building Docker image..."
	docker build -t myapp:latest .

build_gcp:
	docker build -t $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) .

push : build_gcp
	docker push $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

deploy: push
	gcloud run deploy $(IMAGE_NAME) \
		--image $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) \
		--platform managed \
		--region $(LOCATION) \
		--allow-unauthenticated \
		--project $(PROJECT_ID)