all: dev-api-docs

build-api-docs:
		aglio -i api-docs/api.apib -o api-docs/index.html

dev-api-docs:
		aglio -i api-docs/api.apib -o api-docs/index.html --server

tar_name := farnsworth-api.$(shell date +"%Y%M%d%H%m%s").tgz
publish-api-docs: build-api-docs
		tar cfz $(tar_name) api-docs/
		scp $(tar_name) cgc-docs@cgc-api-docs.seclab.cs.ucsb.edu:
