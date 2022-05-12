import uuid
from django.db import models

CHAR_FIELD_MAX_LENGTH = 50

class User(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField('Name', max_length = CHAR_FIELD_MAX_LENGTH)
    surname = models.CharField('Surname', max_length = CHAR_FIELD_MAX_LENGTH)
    login = models.CharField(max_length = CHAR_FIELD_MAX_LENGTH)
    password = models.CharField(max_length = CHAR_FIELD_MAX_LENGTH)

    def __str__(self):
        return ' '.join([self.name, self.surname])