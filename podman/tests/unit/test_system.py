import unittest

import requests_mock

from podman import PodmanClient


class SystemTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.client = PodmanClient(base_url="http+unix://localhost:9999")

    def tearDown(self) -> None:
        super().tearDown()

        self.client.close()

    @requests_mock.Mocker()
    def test_df(self, mock):
        body = {
            "Containers": [
                {"ContainerID": "f1fb3564c202"},
                {"ContainerID": "779afab684c7"},
            ],
            "Images": [
                {"ImageID": "118cc2c68ef5"},
                {"ImageID": "a6b4a8255f9e"},
            ],
            "Volumes": [
                {"VolumeName": "27df59163be8"},
                {"VolumeName": "77a83a10f86e"},
            ],
        }

        mock.get(
            "http+unix://localhost:9999/v3.0.0/libpod/system/df",
            json=body,
        )

        actual = self.client.df()
        self.assertDictEqual(actual, body)

    @requests_mock.Mocker()
    def test_info(self, mock):
        body = {
            "host": {
                "arch": "amd65",
                "os": "linux",
            }
        }
        mock.get("http+unix://localhost:9999/v3.0.0/libpod/system/info", json=body)

        actual = self.client.info()
        self.assertDictEqual(actual, body)

    @requests_mock.Mocker()
    def test_ping(self, mock):
        mock.head("http+unix://localhost:9999/v3.0.0/libpod/_ping")
        self.assertTrue(self.client.ping())

    @requests_mock.Mocker()
    def test_version(self, mock):
        body = {
            "APIVersion": "3.0.0",
            "MinAPIVersion": "3.0.0",
            "Arch": "amd64",
            "Os": "linux",
        }
        mock.get("http+unix://localhost:9999/v3.0.0/libpod/version", json=body)
        self.assertDictEqual(self.client.version(), body)


if __name__ == '__main__':
    unittest.main()
