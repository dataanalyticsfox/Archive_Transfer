# -*- coding: utf-8 -*-
import os
import json
import requests
import assert_status_code as asc

# this script takes metadata from capture_metadata and creates a dataset on dh using Instrument name as title

# Need UUID and TID of Access Scope Taxonomy
# location: /devel/taxonomy_term/1613
internal_pnnl_tid = '1234'
internal_pnnl_uuid = '4a6baba6-8ff2-440c-b8a7-7acbf9ea6ef7'
admin_uid = '77a7a5d5-6444-4762-b5df-9000cc9f32c2'

# Information Release Number is static. This is specific to IRs from legacy datahub site.
ir_legacy_number = 'PNNL-SA-12345'

# POST json api to base URL


def create_datasets(metadata, title, base_url, headers):
    du_resp = requests.post(
        f'{base_url}/jsonapi/node/data_set',
        json={
            'data': {
                'type': 'node--data_set',
                'attributes': {
                    'title': title,
                    'body': metadata,
                },
                'relationships': {
                    'field_access_scope': {
                        'data': [
                            {'type': 'taxonomy_term--access_scope',
                             'id': internal_pnnl_uuid,
                                'meta': {
                                    'drupal_internal__target_id': internal_tid
                                }
                             }
                        ]
                    },
                    'field_pac_data_set_image': {
                        'data': {
                            'type': 'media--image',
                            'id': 'abd2022d-db4d-47f4-8d57-6c638b2e4c61',
                            'meta': {
                                'drupal_internal__target_id': 450
                            }
                        },
                    },
                    'uid': {
                        'data':
                            {'id': admin_uid,
                             'type': 'user--user',
                             }
                    },
                },
            },
        },
        headers=headers
    )
    asc.assert_status_code(du_resp, 201)
    # end of required dataset api call
    print(f'Success! metadata {title} added to Datahub')


if __name__ == '__main__':
    create_datasets(metadata, title, base_url, headers)
