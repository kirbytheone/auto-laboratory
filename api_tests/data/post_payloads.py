def get_create_post_payload(title: str, body: str, user_id: int):
    return {
        'title': title,
        'body': body,
        'userId': user_id,
    }
