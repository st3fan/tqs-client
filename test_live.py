# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import time

import pytest
import requests
import requests.exceptions

import tqs


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False


@pytest.fixture(scope="session")
def endpoint_url(docker_ip, docker_services):
    url = "http://%s:%d" % (docker_ip, docker_services.port_for("tqs", 8080))
    docker_services.wait_until_responsive(timeout=15.0, pause=0.1, check=lambda: is_responsive(url))
    return url


def random_queue(endpoint_url):
    return tqs.Queue(endpoint_url, "test-%s" % str(int(time.time() * 1000000)))


@pytest.fixture
def queue(endpoint_url):
    queue = random_queue(endpoint_url)
    queue.create()
    return queue


def test_queue_exists(queue):
    assert queue.exists() == True


def test_queue_exists_not(endpoint_url):
    queue = tqs.Queue(endpoint_url, "doesnotexist")
    assert queue.exists() == False


def test_queue_create(endpoint_url):
    queue = random_queue(endpoint_url)
    assert queue.exists() == False
    queue.create()
    assert queue.exists() == True


def test_body_encoding_str(queue):
    queue.put("This is plain text")
    m = queue.get()
    assert m is not None
    assert type(m.body) == str
    assert m.body == "This is plain text"

def test_body_encoding_list(queue):
    queue.put([1,2,3])
    m = queue.get()
    assert m is not None
    assert type(m.body) == list
    assert m.body == [1,2,3]

def test_body_encoding_dict(queue):
    queue.put({"foo": 42})
    m = queue.get()
    assert m is not None
    assert type(m.body) == dict
    assert m.body == {"foo": 42}

def test_body_encoding_bytes(queue):
    queue.put(b"Cheese")
    m = queue.get()
    assert m is not None
    assert type(m.body) == bytes
    assert m.body == b"Cheese"
