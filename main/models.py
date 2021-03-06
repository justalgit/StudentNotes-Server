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


class Group(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.TextField('Title')
    description = models.TextField('Description', blank = True, null = True)
    last_modified_date = models.BigIntegerField('Last modified date')
    is_editable = models.BooleanField('Is editable')
    is_private = models.BooleanField('Is private')
    creator = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_creator'
    )
    last_modified_user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_last_modified_user'
    )

    def __str__(self):
        return self.title


class Event(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.TextField('Title')
    description = models.TextField('Description', blank = True, null = True)
    event_date = models.BigIntegerField('Event date')
    last_modified_date = models.BigIntegerField('Last modified date')
    is_editable = models.BooleanField('Is editable')
    user_priority = models.PositiveSmallIntegerField('User priority', default = 1)
    weighted_priority = models.IntegerField('Weighted priority', default = 1)
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_author'
    )
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        related_name = '%(class)s_group'
    )
    last_modified_user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_last_modified_user'
    )

    def __str__(self):
        return self.title


class Request(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    message = models.TextField('Message', blank = True, null = True)
    request_date = models.BigIntegerField('Request date')
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_author'
    )
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        related_name = '%(class)s_group'
    )

    def __str__(self):
        return "Request from user {} to group {}".format(self.author, self.group)


class UserGroupRelation(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_user'
    )
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        related_name = '%(class)s_group'
    )

    def __str__(self):
        return "Relation between user {} and group {}".format(self.user, self.group)

    class Meta:
        unique_together = ('group', 'user')


class EventPriority(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_user'
    )
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        related_name = '%(class)s_event'
    )
    user_priority = models.IntegerField(default = 1, null=True)
    times_checked = models.IntegerField(default = 0, null=True)

    def __str__(self):
        return "Event {} priority for {}".format(self.event, self.user)

    class Meta:
        unique_together = ('event', 'user')
