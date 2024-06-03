# proj_1 documentation!

## Description

Structural Design Automatation with ML and APIs

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://ceie_proj_1/data/`.
* `make sync_data_down` will use `aws s3 sync` to recursively sync files from `s3://ceie_proj_1/data/` to `data/`.


