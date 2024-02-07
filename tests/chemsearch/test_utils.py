import socket

import pytest

from chemsearch import utils


class TestGetIPAddresses:
    @pytest.fixture
    def address_info(self):
        return [
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_STREAM: 1>",
                6,
                "",
                ("192.168.82.96", 5000),
            ),
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_DGRAM: 2>",
                17,
                "",
                ("192.168.82.96", 5000),
            ),
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_RAW: 3>",
                0,
                "",
                ("192.168.82.96", 5000),
            ),
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_STREAM: 1>",
                6,
                "",
                ("192.168.28.88", 5000),
            ),
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_DGRAM: 2>",
                17,
                "",
                ("192.168.28.88", 5000),
            ),
            (
                "<AddressFamily.AF_INET: 2>",
                "<SocketKind.SOCK_RAW: 3>",
                0,
                "",
                ("192.168.28.88", 5000),
            ),
        ]

    def test_completes(self, mocker, address_info):
        mock = mocker.patch.object(socket, "getaddrinfo", autospec=True)
        mock.return_value = address_info

        utils.get_ip_addresses("dummy-chemsearch.default.svc.cluster.local", 5000)

    def test_returns_expected_ip_addresses(self, mocker, address_info):
        mock = mocker.patch.object(socket, "getaddrinfo", autospec=True)
        mock.return_value = address_info

        expected = ["192.168.28.88", "192.168.82.96"]

        actual = utils.get_ip_addresses(
            "dummy-chemsearch.default.svc.cluster.local", 5000
        )

        assert sorted(actual) == sorted(expected)

    def test_calls_getaddrinfo_with_expected_args(self, mocker, address_info):
        mock = mocker.patch.object(socket, "getaddrinfo", autospec=True)
        mock.return_value = address_info

        utils.get_ip_addresses("dummy-chemsearch.default.svc.cluster.local", 5000)

        mock.assert_called_once_with("dummy-chemsearch.default.svc.cluster.local", 5000)
