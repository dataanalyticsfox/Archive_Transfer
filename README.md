# Single Archive Transfer
- We are migrating data from legacy datahub site to current datahub site.
- Input is one transaction_id from legacy datahub site and your API key. Enter Postgres credentials to connections.ini file.
- Output is an API call to Datahub to post legacy datahub site data package.
- The legacy Datahub site runs on PosgreSQL and we use Python Requests library to scrape legacy datahub site. The current Datahub site uses JSON API and MariaDB.

## main.py
- User must manually change transaction_id (legacy datahub), select base_url, and enter user api-key for this script to function.
- User must also create a connections.ini file to store Posgres and Legacy Datahub connections. See [connections.ini](#connections.ini) section below
- `python3 main.py` on terminal (Mac)

## query_db.py
- This module queries the archive PostgreSQL database one transaction_id at a time. This returns a JSON array with id, path, hashsum, hashtype, size, mimetype, mtime. There can be multiple rows per transaction id.
- Requires user database connection credentials in connections.ini file
- [Local Database Connection Documentaion](https://devops.pnnl.gov/datahub/development/workspaces/carrie-minerich/knowledge/-/wikis/Setting-up-a-local-postgres-connection-for-Mac)

## capture_metadata.py
- This module scrapes legacy datahub using transaction_id. Output is a string of results
- Dataset title is "Instrument Name" value. Title is a spliced string between "Instrument Name" and "Project ID".

## create_dataset.py
- This module takes the metadata string returned from capture_metadata.py and uses the Drupal JSON API to POST a pacifica_data_set to datahub.

## create_dataupload.py
- This module takes the query returned from query_db.py and uses the Drupal JSON API to POST a pacifica_data_upload to datahub.
- This module also inputs the title generated from the capture_metadata.py module.

## merge_ds_to_du.py
- Two functions, GET_dataset_ids and GET_uploads_id, to return drupal_internal_nid's based on capture_metadata.py and create_dataset.py API POST requests.
- With (inputs), PATCH request to link data upload to dataset.

------------------------------

## assert_status_code.py
- A module to document errors with API calls.
- error.json file will be created in directory tree with traceback

## connections.ini
- User must create a ini file to store local database and legacy datahub connection strings.
- This file added to .gitignore

## config.py
- Reads connections.ini file and returns connection params as a dict.
