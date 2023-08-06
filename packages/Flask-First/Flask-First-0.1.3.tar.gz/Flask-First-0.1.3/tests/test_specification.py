from flask_first import Specification


def test_specification__load_from_yaml(fx_config):
    spec = Specification(fx_config.PATH_TO_SPEC)
    assert spec
    assert spec.spec["info"]["title"] == "Simple API for testing Flask-First"


def test_specification__config_param(fx_app, fx_client):
    @fx_app.specification
    def bad_response() -> dict:
        return {'message': 'OK', 'non_exist_field': 'BAD'}

    fx_app.debug = 0
    fx_app.testing = 0

    assert fx_client.get('/bad_response').status_code == 500
