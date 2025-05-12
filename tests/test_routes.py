from app import create_app

def test_index_route():
    app = create_app()
    app.testing= True
    client = app.test_client()

    response = client.get('/')
    assert response.status_code in [200, 302]