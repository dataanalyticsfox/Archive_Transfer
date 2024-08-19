# -*- coding: utf-8 -*-

# upload title should match the dataset and append at the end "upload"
import assert_status_code as asc
import json
import requests


def create_uploads(query_results, title, base_url, headers):
    print('Upload for ' + title)

    # Create upload based using the path as the title
    du_resp = requests.post(
        f'{base_url}/jsonapi/node/data_upload/',
        json={
            'data': {
                'type': 'node--pacifica_data_upload',
                'attributes': {
                    'title': 'Upload for ' + title,  # based on existing title in capture_metadata.py
                    'field_pac_file_metadata': json.dumps(query_results),
                    'moderation_state': 'draft'
                },
            }
        },
        headers=headers
    )
    asc.assert_status_code(du_resp, 201)

    # push the upload to complete. multiple rows from sql query
    for transition in ['upload', 'commit', 'published']:
        dup_resp = requests.patch(
            f"{base_url}/jsonapi/node/data_upload/{du_resp.json()['data']['id']}",
            json={
                'data': {
                    'type': 'node--data_upload',
                    'id': du_resp.json()['data']['id'],
                    'attributes': {
                        'moderation_state': transition
                    }
                }
            },
            headers=headers
        )
    asc.assert_status_code(dup_resp, 200)
    print(f'Success! {title} dataset uploaded')


if __name__ == '__main__':
    create_uploads(query_results, title, base_url, headers)
