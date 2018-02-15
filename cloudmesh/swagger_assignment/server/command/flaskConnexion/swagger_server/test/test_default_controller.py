# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.entities import ENTITIES  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_command_post(self):
        """Test case for command_post

        
        """
        entities = ENTITIES()
        response = self.client.open(
            '/api/{command}'.format(command='command_example'),
            method='POST',
            data=json.dumps(entities),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
