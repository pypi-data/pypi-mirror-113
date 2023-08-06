import time
from unittest import TestCase
from digital_thought_commons import settings


class TestPersistentSettingStore(TestCase):

    def test_store(self):
        setting = settings.PersistentSettingStore('./persistent.settings')
        print(setting.store('test2', {'bob': True}))
        time.sleep(3)
        print(setting.get('test2', {'bob': False}))

