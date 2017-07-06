"""

"""

from __future__ import print_function

import os
import time
from nose.tools import raises
import sigfoxapi

sigfoxapi.DEBUG = True

SIGFOX_LOGIN_ID = os.environ['SIGFOX_LOGIN_ID']
SIGFOX_PASSWORD = os.environ['SIGFOX_PASSWORD']
SIGFOX_DEVICETYPE_ID = os.environ['SIGFOX_DEVICETYPE_ID']
SIGFOX_DEVICE_ID = os.environ['SIGFOX_DEVICE_ID']
SIGFOX_USER_ID = os.environ['SIGFOX_USER_ID']
SIGFOX_GROUP_ID = os.environ['SIGFOX_GROUP_ID']

TIMESTAMP = time.strftime('%Y-%m-%d %H:%M:%S')


@raises(sigfoxapi.SigfoxApiBadRequest)
def test_sigfoxapi_autherror():
    s = sigfoxapi.Sigfox('wrong_login_id', 'wrong_password')
    s.group_info(SIGFOX_GROUP_ID)


@raises(sigfoxapi.SigfoxApiAuthError)
def test_sigfoxapi_autherror():
    s = sigfoxapi.Sigfox('012345678901234567891234', '12345678901234567890123456789012')
    s.group_info(SIGFOX_GROUP_ID)


# Doesn work with @raises
def test_sigfoxapi_notfound():
    s = sigfoxapi.Sigfox(SIGFOX_LOGIN_ID, SIGFOX_PASSWORD)
    try:
        s.group_info('123456789012345678901234')
    except sigfoxapi.SigfoxApiNotFound:
        pass


@raises(sigfoxapi.SigfoxApiError)
def test_sigfoxapi_apierror():
    s = sigfoxapi.Sigfox(SIGFOX_LOGIN_ID, SIGFOX_PASSWORD)
    s.group_info('does_not_exist')

# TODO: Add more exceotion testing

class _TestSigfoxBase(object):
    def setup(self):
        self.s = sigfoxapi.Sigfox(SIGFOX_LOGIN_ID, SIGFOX_PASSWORD)
        sigfoxapi.RETURN_OBJECTS = False


class _TestSigfoxBaseObject(object):
    def setup(self):
        self.s = sigfoxapi.Sigfox(SIGFOX_LOGIN_ID, SIGFOX_PASSWORD)
        sigfoxapi.RETURN_OBJECTS = True


class TestSigfoxUsers(_TestSigfoxBase):

    def test_user_list(self):
        users = self.s.user_list(SIGFOX_GROUP_ID)
        assert isinstance(users, list)
        assert len(users) == 1
        assert users[0]['timezone'] == 'Australia/Melbourne'

#    @raises(sigfoxapi.SigfoxApiError)
#    def test_user_list_invalid_groupid(self):
#        self.s.user_list('invalid')


class TestSigfoxUsersObject(_TestSigfoxBaseObject):

    def test_user_list(self):
        users = self.s.user_list(SIGFOX_GROUP_ID)
        assert isinstance(users, sigfoxapi.Object)
        assert len(users) == 1
        assert users[0].timezone == 'Australia/Melbourne'


class TestSigfoxGroups(_TestSigfoxBase):

    def test_group_info(self):
        group = self.s.group_info(SIGFOX_GROUP_ID)
        assert isinstance(group, dict)
        assert group['id'] == SIGFOX_GROUP_ID

    def test_group_list(self):
        groups = self.s.group_list()
        assert isinstance(groups, list)
        assert len(groups) == 0


class TestSigfoxGroupsObject(_TestSigfoxBaseObject):

    def test_group_info(self):
        group = self.s.group_info(SIGFOX_GROUP_ID)
        assert isinstance(group, sigfoxapi.Object)
        assert group.id == SIGFOX_GROUP_ID

    def test_group_list(self):
        groups = self.s.group_list()
        assert isinstance(groups, sigfoxapi.Object)
        assert len(groups) == 0


class TestSigfoxDevicetypes(_TestSigfoxBase):

    def test_devicetype_info_and_edit(self):
        devicetype = self.s.devicetype_info(SIGFOX_DEVICETYPE_ID)
        assert isinstance(devicetype, dict)
        assert devicetype['id'] == SIGFOX_DEVICETYPE_ID
        assert devicetype['description'] != TIMESTAMP

        params = {'id': SIGFOX_DEVICETYPE_ID,
                  'description': TIMESTAMP}

        self.s.devicetype_edit(SIGFOX_DEVICETYPE_ID, params)
        devicetype = self.s.devicetype_info(SIGFOX_DEVICETYPE_ID)
        assert devicetype['description'] == TIMESTAMP

    def test_devicetype_list(self):
        devicetypes = self.s.devicetype_list()
        assert isinstance(devicetypes, list)

        found = [devicetype for devicetype in devicetypes
                 if devicetype['id'] == SIGFOX_DEVICETYPE_ID]
        assert len(found) == 1

    def test_devicetype_errors(self):
         errors = self.s.devicetype_errors(SIGFOX_DEVICETYPE_ID)
         assert isinstance(errors, list)
         if len(errors) > 0:
             pass   # TODO

    def test_devicetype_warnings(self):
         warnings = self.s.devicetype_warnings(SIGFOX_DEVICETYPE_ID)
         assert isinstance(warnings, list)
         if len(warnings) > 0:
             pass   # TODO

    def test_devicetype_messages(self):
         messages = self.s.devicetype_messages(SIGFOX_DEVICETYPE_ID)
         assert isinstance(messages, list)
         if len(messages) > 0:
             for message in messages:
                 assert isinstance(message['data'], str)
                 assert isinstance(message['device'], str)
                 assert isinstance(message['linkQuality'], str)
                 assert isinstance(message['snr'], str)
                 assert isinstance(message['time'], int)


class TestSigfoxDevicetypesObject(_TestSigfoxBaseObject):

    def test_devicetype_info(self):
        devicetype = self.s.devicetype_info(SIGFOX_DEVICETYPE_ID)
        assert isinstance(devicetype, sigfoxapi.Object)
        assert devicetype.id == SIGFOX_DEVICETYPE_ID

    def test_devicetype_list(self):
        devicetypes = self.s.devicetype_list()
        assert isinstance(devicetypes, sigfoxapi.Object)

        found = [devicetype for devicetype in devicetypes
                 if devicetype.id == SIGFOX_DEVICETYPE_ID]
        assert len(found) == 1

    def test_devicetype_errors(self):
         errors = self.s.devicetype_errors(SIGFOX_DEVICETYPE_ID)
         assert isinstance(errors, sigfoxapi.Object)
         if len(errors) > 0:
             pass   # TODO

    def test_devicetype_warnings(self):
         warnings = self.s.devicetype_warnings(SIGFOX_DEVICETYPE_ID)
         assert isinstance(warnings, sigfoxapi.Object)
         if len(warnings) > 0:
             pass   # TODO

    def test_devicetype_messages(self):
         messages = self.s.devicetype_messages(SIGFOX_DEVICETYPE_ID)
         assert isinstance(messages, sigfoxapi.Object)
         if len(messages) > 0:
             for message in messages:
                 assert isinstance(message.data, str)
                 assert isinstance(message.device, str)
                 assert isinstance(message.linkQuality, str)
                 assert isinstance(message.snr, str)

CALLBACKID = None

class TestSigfoxCallbacks(_TestSigfoxBase):

    def test_callback_0_list_and_edit(self):
        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback['channel'] == 'EMAIL' and
                    callback['message'] == TIMESTAMP]
        assert found == []

        new_callbacks = [
            {
                'channel': 'EMAIL',
                'subject': 'SIGFOXAPI TEST',
                'recipient': 'noone@example.com',
                'message': TIMESTAMP,
                'callbackType': 0,
                'callbackSubtype': 2,
                'enabled': False,
                'sendDuplicate': False,
                'payloadConfig': ''
            }
        ]
        self.s.callback_new(SIGFOX_DEVICETYPE_ID, new_callbacks)

        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback['channel'] == 'EMAIL' and
                    callback['message'] == TIMESTAMP]
        assert len(found) == 1

        global CALLBACKID
        CALLBACKID = found[0]['id']

    def test_callback_1_enable(self):
        self.s.callback_enable(SIGFOX_DEVICETYPE_ID, CALLBACKID)
        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback['channel'] == 'EMAIL' and
                    callback['message'] == TIMESTAMP]
        assert found[0]['enabled'] is True

    def test_callback_2_disable(self):
        self.s.callback_disable(SIGFOX_DEVICETYPE_ID, CALLBACKID)
        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback['channel'] == 'EMAIL' and
                    callback['message'] == TIMESTAMP]
        assert found[0]['enabled'] is False

    def test_callback_2_disable(self):
        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        for callback in callbacks:
            if callback['channel'] == 'EMAIL' and callback['subject'] == 'SIGFOXAPI TEST':
                self.s.callback_delete(SIGFOX_DEVICETYPE_ID, callback['id'])

        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback['channel'] == 'EMAIL' and
                    callback['subject'] == 'SIGFOXAPI TEST']

        assert len(found) == 0


class TestSigfoxCallbacksObject(_TestSigfoxBaseObject):

    def test_callback_list(self):
        callbacks = self.s.callback_list(SIGFOX_DEVICETYPE_ID)
        found = [callback for callback in callbacks
                 if callback.channel == 'EMAIL' and
                    callback.message == TIMESTAMP]
        assert found == []


class TestSigfoxDevices(_TestSigfoxBase):

    def test_device_list(self):
        devices = self.s.device_list(SIGFOX_DEVICETYPE_ID)
        assert isinstance(devices, list)
        found = [device for device in devices if device['id'] == SIGFOX_DEVICE_ID]
        assert len(found) == 1
        assert isinstance(found[0], dict)

    def test_device_info(self):
        device = self.s.device_info(SIGFOX_DEVICE_ID)
        assert device['id'] == SIGFOX_DEVICE_ID

    def test_device_tokenstate(self):
        tokenstate = self.s.device_tokenstate(SIGFOX_DEVICE_ID)
        assert tokenstate['code'] in [0,1,2]

    def test_device_messages(self):
         messages = self.s.device_messages(SIGFOX_DEVICE_ID)
         assert isinstance(messages, list)
         if len(messages) > 0:
             for message in messages:
                 assert isinstance(message['data'], str)
                 assert isinstance(message['device'], str)
                 assert isinstance(message['linkQuality'], str)
                 assert isinstance(message['snr'], str)
                 assert isinstance(message['time'], int)

    def test_device_locations(self):
         locations = self.s.device_locations(SIGFOX_DEVICE_ID)
         assert isinstance(locations, list)
         if len(locations) > 0:
             for location in locations:
                 assert isinstance(location['valid'], bool)

    def test_device_warnings(self):
         warnings = self.s.device_warnings(SIGFOX_DEVICE_ID)
         assert isinstance(warnings, list)

    def test_device_errors(self):
         errors = self.s.device_errors(SIGFOX_DEVICE_ID)
         assert isinstance(errors, list)

    def test_device_networkstate(self):
        networkstate = self.s.device_networkstate(SIGFOX_DEVICE_ID)
        assert isinstance(networkstate, dict)
        assert networkstate['networkStatus'] in ['OK', 'NOK']

    def test_device_messagemetrics(self):
        metrics = self.s.device_messagemetrics(SIGFOX_DEVICE_ID)
        assert isinstance(metrics, dict)
        assert isinstance(metrics['lastDay'], int)
        assert isinstance(metrics['lastMonth'], int)
        assert isinstance(metrics['lastWeek'], int)

    def test_device_consumptions(self):
        consumptions = self.s.device_messagemetrics(SIGFOX_DEVICE_ID)
        assert isinstance(consumptions, dict)


class TestSigfoxDevicesObject(_TestSigfoxBaseObject):

    def test_device_list(self):
        devices = self.s.device_list(SIGFOX_DEVICETYPE_ID)
        assert isinstance(devices, sigfoxapi.Object)
        found = [device for device in devices if device.id == SIGFOX_DEVICE_ID]
        assert len(found) == 1
        assert isinstance(found[0], sigfoxapi.Object)

    def test_device_info(self):
        device = self.s.device_info(SIGFOX_DEVICE_ID)
        assert device.id == SIGFOX_DEVICE_ID

    def test_device_tokenstate(self):
        tokenstate = self.s.device_tokenstate(SIGFOX_DEVICE_ID)
        assert tokenstate.code in [0,1,2]

    def test_device_messages(self):
         messages = self.s.device_messages(SIGFOX_DEVICE_ID)
         assert isinstance(messages, sigfoxapi.Object)
         if len(messages) > 0:
             for message in messages:
                 assert isinstance(message.data, str)
                 assert isinstance(message.device, str)
                 assert isinstance(message.linkQuality, str)
                 assert isinstance(message.snr, str)
                 assert isinstance(message.time, int)

    def test_device_locations(self):
         locations = self.s.device_locations(SIGFOX_DEVICE_ID)
         assert isinstance(locations, sigfoxapi.Object)
         if len(locations) > 0:
             for location in locations:
                 assert isinstance(location.valid, bool)

    def test_device_warnings(self):
         warnings = self.s.device_warnings(SIGFOX_DEVICE_ID)
         assert isinstance(warnings, sigfoxapi.Object)

    def test_device_errors(self):
         errors = self.s.device_errors(SIGFOX_DEVICE_ID)
         assert isinstance(errors, sigfoxapi.Object)

    def test_device_networkstate(self):
        networkstate = self.s.device_networkstate(SIGFOX_DEVICE_ID)
        assert isinstance(networkstate, sigfoxapi.Object)
        assert networkstate.networkStatus in ['OK', 'NOK']

    def test_device_messagemetrics(self):
        metrics = self.s.device_messagemetrics(SIGFOX_DEVICE_ID)
        assert isinstance(metrics, sigfoxapi.Object)
        assert isinstance(metrics.lastDay, int)
        assert isinstance(metrics.lastMonth, int)
        assert isinstance(metrics.lastWeek, int)

    def test_device_consumptions(self):
        consumptions = self.s.device_messagemetrics(SIGFOX_DEVICE_ID)


class TestSigfoxCoverage(_TestSigfoxBase):

    def test_coverage_redundancy(self):
        redundancy = self.s.coverage_redundancy(43.415, 1.9693, mode='OUTDOOR')
        assert redundancy['redundancy'] > 1

    def test_coverage_predictions(self):
        predictions = self.s.coverage_predictions(43.415, 1.9693)
        assert len(predictions['margins']) == 3


class TestSigfoxCoverageObject(_TestSigfoxBaseObject):

    def test_coverage_redundancy(self):
        redundancy = self.s.coverage_redundancy(43.415, 1.9693, mode='OUTDOOR')
        assert redundancy.redundancy > 1

    def test_coverage_predictions(self):
        predictions = self.s.coverage_predictions(43.415, 1.9693)
        assert len(predictions.margins) == 3

