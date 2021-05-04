import pytest

from flaskr import app


def test_home(client):
	response = client.get('/')
	print(response)
	json_data = response.get_json()

	assert json_data["data"] == "This is the InkChat server"
		