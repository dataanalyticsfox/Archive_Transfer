# -*- coding: utf-8 -*-
import assert_status_code as asc
import requests


# arrays needed to store values
dataset_int_nids = []
dataset_id = []
upload_int_ids = []
upload_ids = []

# GET json api to get dataset based on title


def GET_dataset_ids(title, base_url, headers):
    ds_resp = requests.get(
        f'{base_url}/jsonapi/node/data_set',
        params={
            'filter[field-cond][condition][path]': 'title',
            'filter[field-cond][condition][operator]': '=',
            'filter[field-cond][condition][value]': title,
        },
        headers=headers
    )
    asc.assert_status_code(ds_resp, 200)
    # print (ds_resp.json()['data'][0]['attributes']['drupal_internal__nid'])
    dataset_int_nids.append(
        ds_resp.json()['data'][0]['attributes']['drupal_internal__nid'])
    dataset_id.append(ds_resp.json()['data'][0]['id'])

# GET json api to get dataset based on title


def GET_upload_ids(title, base_url, headers):
    ds_resp = requests.get(
        f'{base_url}/jsonapi/node/data_upload',
        params={
            'filter[field-cond][condition][path]': 'title',
            'filter[field-cond][condition][operator]': '=',
            'filter[field-cond][condition][value]': 'Upload for ' + title,
        },
        headers=headers
    )
    asc.assert_status_code(ds_resp, 200)
    upload_int_ids.append(
        ds_resp.json()['data'][0]['attributes']['drupal_internal__nid'])
    upload_ids.append(ds_resp.json()['data'][0]['id'])

# three api calls: one to find dataset title, one to find data upload (using title), and merge both together
# patch request to update dataset with dataset upload
# update to use a unique identifier instead of title? How to verify that dataset and data upload are what we want


def merge_upload_to_dataset(title, base_url, headers):
    GET_dataset_ids(title, base_url, headers)
    GET_upload_ids(title, base_url, headers)

    for (ds_id, up_id, up_int_id) in zip(dataset_id, upload_ids, upload_int_ids):
        print(f'dataset id: {ds_id}')  # this is dataset id
        print(f'upload_id: {up_id}')  # this is upload id
        print(f'drupal iternal target id: {up_int_id}')
        # add dataupload, an IR to dataset
        dup_resp = requests.patch(
            f'{base_url}/jsonapi/node/data_set/' + ds_id,
            json={
                'data': {
                    'type': 'node--data_set',
                    'id': ds_id,
                    'attributes': {
                        'status': True,
                    },
                    'relationships': {
                        'field_information_release_list': {
                            'data': [{
                                'type': 'taxonomy_term--information_release_taxonomy',
                                'id': '84bde9e6-0e5e-4c3d-91fd-e4fa286c7a33',
                                'meta': {
                                    'drupal_internal__target_id': 123456
                                }
                            }],
                        },
                        'field_pac_data_upload': {
                            'data': [{
                                'type': 'node--data_upload',
                                'id': up_id,
                                'meta': {
                                    'drupal_internal__target_id': up_int_id
                                }
                            }],
                        },
                    },
                },
            },
            headers=headers
        )
        asc.assert_status_code(dup_resp, 200)
        print(
            f'Success! {title} Dataset and Data Upload are merged on Datahub')


if __name__ == '__main__':
    merge_upload_to_dataset(title, base_url, headers)
