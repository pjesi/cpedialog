from google.appengine.ext import db
from string import ascii_letters, digits
import hashlib, random

def gen_hash(password, salt=None, algorithm='sha512'):
    hash = hashlib.new(algorithm)
    hash.update(password)
    if not salt:
        salt = ''.join([random.choice(ascii_letters + digits) for _ in range(8)])
    hash.update(salt)
    return (algorithm, salt, hash.hexdigest())

class UserTraits(db.Model):
    last_login = db.DateTimeProperty()
    date_joined = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    is_active = db.BooleanProperty(default=False, required=True)
    is_staff = db.BooleanProperty(default=False, required=True)
    is_superuser = db.BooleanProperty(default=False, required=True)
    password = db.StringProperty()

    @property
    def id(self):
        # Needed for compatibility
        return str(self.key())

    def __unicode__(self):
        return unicode(self.key().id_or_name())

    def __str__(self):
        return unicode(self).encode('utf-8')

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        if not self.has_usable_password():
            return False
        algorithm, salt, hash = self.password.split('$')
        return hash == gen_hash(password, salt, algorithm)[2]

    def set_password(self, password):
        self.password = '$'.join(gen_hash(password))

    @classmethod
    def make_random_password(self, length=16,
            allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        """
        Generates a random password with the given length and given allowed_chars.
        """
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        from random import choice
        return ''.join([choice(allowed_chars) for i in range(length)])


class EmailUserTraits(UserTraits):
    def email_user(self, subject, message, from_email=None):
        """Sends an e-mail to this user."""
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

class EmailUser(EmailUserTraits):
    email = db.StringProperty(multiline=False)
    # This can be used to distinguish between banned users and unfinished
    # registrations
    is_banned = db.BooleanProperty(default=False, required=True)

class User(EmailUserTraits):
    """Default User class that mimics Django's User class."""
    username = db.StringProperty(required=True)
    first_name = db.StringProperty()
    last_name = db.StringProperty()
