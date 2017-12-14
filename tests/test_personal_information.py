from src.blockchain import SecretInformation
import unittest
import jwt


class TestPersonalInformation(unittest.TestCase):
    info = dict(name='Andrew',
                surname='Graham',
                email='andrew@gmail.com',
                phone_number='123-456-7890')
    secret_key = 'happy.lucky'

    def setUp(self):
        self.p_info = SecretInformation(self.secret_key,
                                        **self.info)

    def test_init(self):
        assert self.p_info.key == self.secret_key
        encoded = self.p_info.encoded_info
        string = self.p_info.info_str
        assert encoded
        assert isinstance(string, str)
        decode = jwt.decode(encoded, self.secret_key)
        assert decode.get('name') == self.info.get('name')

    def test_positive_validation(self):
        assert self.p_info.is_valid(**self.info)

    def test_negative_validation(self):
        info = dict(name='John',
                    surname='Smith',
                    email='j.smith@gmail.com',
                    phone_number='123-456-7890')
        res = self.p_info.is_valid(**info)
        assert not res





