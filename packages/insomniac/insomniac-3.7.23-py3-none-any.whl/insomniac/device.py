from insomniac.device_facade import create_device
from insomniac.typewriter import Typewriter
from insomniac.utils import *


class DeviceWrapper(object):
    device = None

    def __init__(self, device_id, old_uiautomator, wait_for_device, app_id, app_name, dont_set_typewriter):
        self.device_id = device_id
        if app_name is None:
            self.app_id = app_id
        else:
            from insomniac.extra_features.utils import get_package_by_name
            self.app_id = get_package_by_name(self.device_id, app_name)
            if self.app_id is not None:
                print(f"Found app id by app name: {self.app_id}")
            else:
                print(COLOR_FAIL + "You provided app name but there's no app with such name" + COLOR_ENDC)
                self.app_id = app_id
        self.app_name = app_name
        self.old_uiautomator = old_uiautomator

        self.create(wait_for_device, dont_set_typewriter)

    def get(self):
        return self.device

    def create(self, wait_for_device, dont_set_typewriter):
        if not check_adb_connection(device_id=self.device_id, wait_for_device=wait_for_device):
            return None

        typewriter = Typewriter(self.device_id)
        if not dont_set_typewriter:
            typewriter.set_adb_keyboard()

        device = create_device(self.old_uiautomator, self.device_id, self.app_id, typewriter)
        if device is None:
            return None

        self.device = device

        return self.device
