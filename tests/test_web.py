from web.app import create_app
def test_health_route():
 response=create_app().test_client().get('/health'); assert response.status_code==200 and response.json['status']=='ok'
