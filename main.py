# -*- coding: utf-8 -*-
# One main python file to run this entire project
# required inputs: Must change transaction_id to the ID you want to migrate to Datahub.
# required: must designate URL and api-key in main.py
# required: must add Postgres database and legacy datahub credentials to connections.ini file
import query_db
import capture_metadata as cm
import create_dataset as cd
import create_dataupload as cdup
import merge_ds_to_du as mdd


def main(transaction_id, base_url, headers):
    # transaction_id returns query from legacy datahub site
    query_results = query_db.main(transaction_id)
    # capture_metadata returns metadata AND title as variables
    metadata, title = cm.get_metadata(transaction_id)

    create_ds = cd.create_datasets(
        metadata, title, base_url, headers)  # create dataset in datahub
    # create data upload in datahub
    upload_ds = cdup.create_uploads(query_results, title, base_url, headers)

    # patch api request to link data upload to dataset
    final = mdd.merge_upload_to_dataset(title, base_url, headers)


if __name__ == '__main__':

    transaction_id = 903

    # Site to get and post
    base_url = 'https://dhdev01.abc'

    # admin Api-key is required
    # make sure you have the api access role.
    auth_key = '84bde9e6-0e5e-4c3d-91fd-e4fa286c7a33'

    # Header for json file
    headers = {
        'api-key': auth_key,
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }

    main(transaction_id, base_url, headers)
