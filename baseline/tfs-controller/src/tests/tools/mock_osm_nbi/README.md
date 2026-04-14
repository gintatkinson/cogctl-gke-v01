# Mock OSM NBI

Basic OSM NBI to test OSM Client component.

## Relevant commands:

- Build the component for testing
```bash
docker buildx build -t "mock-osm-nbi:test" -f ./src/tests/tools/mock_osm_nbi/Dockerfile ./src/tests/tools/mock_osm_nbi
```

- Run the component
```bash
docker network create -d bridge teraflowbridge
docker run --name mock_osm_nbi -d --network=teraflowbridge --env LOG_LEVEL=DEBUG --env FLASK_ENV=development mock_osm_nbi:test
docker logs mock_osm_nbi
```
