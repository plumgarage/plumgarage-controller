from django.utils.crypto import get_random_string

def generate_secret_key(location):
    f = open(location, 'w')
    key = get_random_string(64)
    f.write("SECRET_KEY = '%s'" % key)
    f.close()
