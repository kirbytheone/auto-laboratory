import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_task_api_orders_by_title_ascending(api_client, create_user, create_task):
    user = create_user(username='ordering_title_user')

    create_task(owner=user, title='Zulu Task')
    create_task(owner=user, title='Alpha Task')
    create_task(owner=user, title='Middle Task')

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'ordering': 'title'},
    )

    assert response.status_code == 200

    returned_titles = [
        task['title'] for task in response.data['results']
    ]

    assert returned_titles == ['Alpha Task', 'Middle Task', 'Zulu Task']

@pytest.mark.django_db
def test_task_api_orders_by_title_descending(api_client, create_user, create_task):
    user = create_user(username='ordering_desc_user')

    create_task(owner=user, title='Zulu Task')
    create_task(owner=user, title='Alpha Task')
    create_task(owner=user, title='Middle Task')

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'ordering': '-title'},
    )

    assert response.status_code == 200

    returned_titles = [
        task['title'] for task in response.data['results']
    ]

    assert returned_titles == ['Zulu Task', 'Middle Task', 'Alpha Task']

@pytest.mark.django_db
def test_task_api_orders_filtered_results(api_client, create_user, create_task):
    user = create_user(username='filtered_ordering_user')

    create_task(
        owner=user,
        title='Zulu Todo Task',
        status='TODO',
    )
    create_task(
        owner=user,
        title='Alpha Todo Task',
        status='TODO',
    )
    create_task(
        owner=user,
        title='Bravo Done Task',
        status='DONE',
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {
            'status': 'TODO',
            'ordering': 'title',
        },
    )

    assert response.status_code == 200
    assert response.data['count'] == 2

    returned_titles = [ task['title'] for task in response.data['results'] ]

    assert returned_titles == ['Alpha Todo Task', 'Zulu Todo Task']
























