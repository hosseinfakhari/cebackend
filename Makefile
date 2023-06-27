build-docker:
	docker build -t cebackend . --no-cache

build-frontend:
	cd frontend && rm -rf build && npm run build && cp build/index.html templates/frontend && cp -r build/static static && cp build/manifest.json static