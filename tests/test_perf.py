import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_home_page_perf(benchmark, client):
    result = benchmark(lambda: client.get('/'))
    assert result.status_code == 200
