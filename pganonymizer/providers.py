import random
import string
import uuid
from hashlib import md5

from faker import Faker
from six import with_metaclass

from pganonymizer.exceptions import InvalidProvider, InvalidProviderArgument

PROVIDERS = []

fake_data = Faker()


def get_provider(provider_config):
    """
    Return a provider instance, according to the schema definition of a field.

    :param dict provider_config: A provider configuration for a single field, e.g.:

        {'name': 'set', 'value': 'Foo'}

    :return: A provider instance
    :rtype: Provider
    """
    def get_provider_class(cid):
        for klass in PROVIDERS:
            if klass.matches(cid):
                return klass
    name = provider_config['name']
    cls = get_provider_class(name)
    if cls is None:
        raise InvalidProvider('Could not find provider with id %s' % name)
    return cls(**provider_config)


class ProviderMeta(type):
    """Metaclass to register all provider classes."""

    def __new__(cls, clsname, bases, attrs):
        newclass = super(ProviderMeta, cls).__new__(cls, clsname, bases, attrs)
        if clsname != 'Provider':
            PROVIDERS.append(newclass)
        return newclass


class Provider(object):
    """Base class for all providers."""

    id = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def matches(cls, name):
        return cls.id.lower() == name.lower()

    def alter_value(self, value):
        raise NotImplementedError


class ChoiceProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider that returns a random value from a list of choices."""

    id = 'choice'

    def alter_value(self, value):
        return random.choice(self.kwargs.get('values'))


class ClearProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to set a field value to None."""

    id = 'clear'

    def alter_value(self, value):
        return None


class FakeProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to generate fake data."""

    id = 'fake'

    @classmethod
    def matches(cls, name):
        return cls.id.lower() == name.split('.')[0].lower()

    def alter_value(self, value):
        func_name = self.kwargs['name'].split('.')[1]
        try:
            func = getattr(fake_data, func_name)
        except AttributeError as exc:
            raise InvalidProviderArgument(exc)
        return func()


class MaskProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider that masks the original value."""

    id = 'mask'
    default_sign = 'X'

    def alter_value(self, value):
        sign = self.kwargs.get('sign', self.default_sign) or self.default_sign
        return sign * len(value)


class MD5Provider(with_metaclass(ProviderMeta, Provider)):
    """Provider to hash a value with the md5 algorithm."""

    id = 'md5'

    def alter_value(self, value):
        return md5(value.encode('utf-8')).hexdigest()

class FiscalCodeProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to hash a fiscal code."""

    id = 'fiscalcode'

    def alter_value(self, value):
        crypt_fiscal_code=md5(value.encode('utf-8')).hexdigest()

        def check_day(numbers):
            if(int(numbers[3])>7):
                numbers[3]=str(1)
            return numbers[3:5]
        
        def check_month(character):
            char_month = ['A','B','C','D','E','H','L','M','P','R','S','T']
            if character in char_month:
                return character
            else:
                index = 4
                return char_month[index]

        def generate_fiscal_code(characters, numbers):
            separator = ''
            generate_fiscal_code = separator.join(characters[0:6]) + separator.join(numbers[0:2]) + check_month(characters[8]) + separator.join(check_day(numbers)) + characters[11] + separator.join(numbers[6:9]) + characters[12]
            return generate_fiscal_code
        
        split_string = []
        n=2
        for index in range(0, len(crypt_fiscal_code), n):
            split_string.append(crypt_fiscal_code[index : index + n])

        characters=[]
        
        for digit in split_string:
            digit_hex = int(digit, 16)
            digit_char = digit_hex % 26
            character = chr(ord('A')+digit_char)
            characters.append(character)

        numbers=[]
        for digit in split_string[6:]:
            digit_hex = int(digit, 16)
            digit_char = digit_hex % 10
            numbers.append(str(digit_char))

        generate_fiscal_code = generate_fiscal_code(characters, numbers)
        return generate_fiscal_code

class VatNumberProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to hash a vat number."""

    id = 'vatnumber'

    def alter_value(self, value):
        vatnumber=value[2:]
        crypt_vat_number=md5(vatnumber.encode('utf-8')).hexdigest()

        split_string = []
        n=2
        for index in range(0, len(crypt_vat_number), n):
            split_string.append(crypt_vat_number[index : index + n])

        numbers=[]
        for digit in split_string:
            digit_hex = int(digit, 16)
            digit_char = digit_hex % 10
            numbers.append(str(digit_char))

        separator = ''
        generate_vat_number = 'IT'+separator.join(numbers[0:9])
        return generate_vat_number

class VatNumberProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to hash a vat number."""

    id = 'fiscalcodebusiness'

    def alter_value(self, value):
        fiscalcode_business=value[0:]
        crypt_fiscalcode_business=md5(fiscalcode_business.encode('utf-8')).hexdigest()

        split_string = []
        n=2
        for index in range(0, len(crypt_fiscalcode_business), n):
            split_string.append(crypt_fiscalcode_business[index : index + n])

        numbers=[]
        for digit in split_string:
            digit_hex = int(digit, 16)
            digit_char = digit_hex % 10
            numbers.append(str(digit_char))

        separator = ''
        generate_fiscalcode_business = separator.join(numbers[0:9])
        return generate_fiscalcode_business
        
class VatNumberProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to hash a vat number."""

    id = 'fiscalcodevat'

    def alter_value(self, value):

        if(value[0].isdigit()):
            #code for fiscalcode legal entity 
            fiscalcode_business=value[0:]
            crypt_fiscalcode_business=md5(fiscalcode_business.encode('utf-8')).hexdigest()

            split_string = []
            n=2
            for index in range(0, len(crypt_fiscalcode_business), n):
                split_string.append(crypt_fiscalcode_business[index : index + n])

            numbers=[]
            for digit in split_string:
                digit_hex = int(digit, 16)
                digit_char = digit_hex % 10
                numbers.append(str(digit_char))

            separator = ''
            generate_fiscalcode_business = separator.join(numbers[0:9])
            return generate_fiscalcode_business
        else:
            #code for fiscalcode natural person
            crypt_fiscal_code=md5(value.encode('utf-8')).hexdigest()

            def check_day(numbers):
                if(int(numbers[3])>7):
                    numbers[3]=str(1)
                return numbers[3:5]
        
            def check_month(character):
                char_month = ['A','B','C','D','E','H','L','M','P','R','S','T']
                if character in char_month:
                    return character
                else:
                    index = 4
                    return char_month[index]

            def generate_fiscal_code(characters, numbers):
                separator = ''
                generate_fiscal_code = separator.join(characters[0:6]) + separator.join(numbers[0:2]) + check_month(characters[8]) + separator.join(check_day(numbers)) + characters[11] + separator.join(numbers[6:9]) + characters[12]
                return generate_fiscal_code
        
            split_string = []
            n=2
            for index in range(0, len(crypt_fiscal_code), n):
                split_string.append(crypt_fiscal_code[index : index + n])

            characters=[]
        
            for digit in split_string:
                digit_hex = int(digit, 16)
                digit_char = digit_hex % 26
                character = chr(ord('A')+digit_char)
                characters.append(character)

            numbers=[]
            for digit in split_string[6:]:
                digit_hex = int(digit, 16)
                digit_char = digit_hex % 10
                numbers.append(str(digit_char))

            generate_fiscal_code = generate_fiscal_code(characters, numbers)
            return generate_fiscal_code

class SetProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to set a random value for phone number."""

    id = 'phonenumberita'

    def alter_value(self, value):
        prefix='+003'
        return prefix+''.join([str(random.randint(0, 9)) for x in range(0,9)])

class SetProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to set a random value for id card."""

    id = 'randomidcard'

    def alter_value(self, value):
        chars = ''.join(random.choice(string.ascii_letters).upper() for x in range(2))
        numbers =''.join([str(random.randint(0, 9)) for x in range(7)])
        return chars+numbers

class SetProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to set a random uuid"""

    id = 'apikey'

    def alter_value(self, value):
        return uuid.uuid4()

class SetProvider(with_metaclass(ProviderMeta, Provider)):
    """Provider to set a static value."""

    id = 'set'

    def alter_value(self, value):
        return self.kwargs.get('value')
