
.PHONY: help
.DEFAULT_GOAL:=help
help:	## display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2 } END{print ""}' $(MAKEFILE_LIST)

run:  ## run production container stack
	docker compose up --build
build:  ## build test containers (needed for `make shell`)
	docker compose build
shell:  ## development shell (mounting '.' to workdir) (no `nginx`)
	docker compose run --rm -it --volumes ${PWD}:/app --service-ports web_dependency_api /bin/sh
run_local:  ## launch app (when in `shell`)
	python3 -m sanic --host 0.0.0.0 app:app --debug --noisy-exceptions --no-motd --single-process
	# --verbosity

.PHONY: cloc
cloc:  ## count lines of code stats
	cloc --vcs=git
