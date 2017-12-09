from src.blockchain import PersonalInformation
import unittest


class TestPersonalInformation(unittest.TestCase):
    info = dict(name='Andrew',
                surname='Graham',
                email='andrew@gmail.com',
                phone_number='123-456-7890')
    secret_key = 'happy.lucky'

    def setUp(self):
        self.p_info = PersonalInformation(self.secret_key,
                                          **self.info)

    def test_personal_information_init(self):
        assert self.p_info.key == self.secret_key
        assert self.p_info.name == self.info.get('name')
        assert self.p_info.surname == self.info.get('surname')
        assert self.p_info.email == self.info.get('email')
        assert self.p_info.phone == self.info.get('phone_number')

    # def test_locking_personal_info(self):


