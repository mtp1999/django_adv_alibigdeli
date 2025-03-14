import pytest
from tests.utils import api_client_authenticated, test_user1, validate_keys, api_client
from django.urls import reverse


def test_get_task_unauthenticated_user_status_401(api_client):
    client = api_client
    url = reverse('app_todo:api_v1:task_list')

    response = client.get(url)
    assert response.status_code == 401


def test_task_CRUD_success(api_client_authenticated):
    client = api_client_authenticated
    url = reverse('app_todo:api_v1:task_list')
    url_detail = 'app_todo:api_v1:task_detail'

    # 1) create a task

    create_data = {
        'title': 'task1',
        'status': True
    }

    response = client.post(path=url, data=create_data, format='json')
    assert response.status_code == 201

    # 2) check the task list

    response = client.get(url)
    assert response.status_code == 200

    response_data = response.data['results']
    task_id = response_data[0]['id']
    expected_keys = ["id", "user", "title", "status", "created_date", "absolute_url"]

    for task in response_data:
        validate_keys(expected_keys, task.keys())

    # 3) update task

    update_data = {
        'id': task_id,
        'title': 'task1 updated',
        'status': False
    }

    response = client.put(path=reverse(url_detail, kwargs={'pk': task_id}), data=update_data, format='json')
    assert response.status_code == 200
    assert response.data["detail"] == "task updated!"

    # 4) get task detail

    response = client.get(path=reverse(url_detail, kwargs={'pk': task_id}))
    assert response.status_code == 200
    response_data = response.data
    assert response_data['id'] == task_id
    assert response_data['title'] == update_data['title']
    assert response_data['status'] == update_data['status']

    expected_keys = ["id", "user", "title", "status", "created_date"]

    validate_keys(expected_keys, response_data.keys())

    # 5) delete task
    response = client.delete(path=reverse(url_detail, kwargs={'pk': task_id}))
    assert response.status_code == 204
    assert response.data['detail'] == "task deleted!"

    # 6) check the task does not exist
    response = client.get(path=reverse(url_detail, kwargs={'pk': task_id}))
    assert response.status_code == 404


