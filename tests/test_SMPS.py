from aws_parameter_uploader.cli import SMPSUploader
from botocore.stub import Stubber, ANY


smps_client = SMPSUploader("testapp", "test")
stubber = Stubber(smps_client.client)
put_expected_params = {
    'Name': ANY,
    'Overwrite': ANY,
    'Type': ANY,
    'Value': ANY
}

fake_put_response_pass = {
    'ResponseMetadata': {
        'RequestId': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'x-amzn-requestid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '2',
            'date': 'Fri, 13 Jan 2017 19:23:00 GMT'
        },
        'RetryAttempts': 0
    }
}


class Test_SMPSFunctions:
    """Test the SMPS Class functions."""

    def test_set_pass(self):
        with stubber:
                stubber.add_response('put_parameter', fake_put_response_pass, put_expected_params)
                response = smps_client.set("datastore", "host", "test.example.com")
        assert response is True

    def test_upload_pass(self):
        with stubber:
            # weirdest thing in the game
            # the stubber response is like a stack of responses
            # it pops a response off the stack each time it's used
            # so let's make a big stack because smps_client.upload does a loop
            for x in range(1, 20):
                stubber.add_response('put_parameter', fake_put_response_pass, put_expected_params)
            response = smps_client.upload("example.ini")
        assert response is True
