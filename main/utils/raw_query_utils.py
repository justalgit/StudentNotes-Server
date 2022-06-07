from main.models import UserGroupRelation


def get_groups_for_user(id):
    return UserGroupRelation.objects.raw(
        "select main_group.* from main_usergrouprelation "
        "join main_group "
        "on main_usergrouprelation.group_id = main_group.id "
        "where user_id = \"{}\"".format(id.replace("-", ""))
    )


def get_events_for_user(id):
    return UserGroupRelation.objects.raw(
        "select e.* from main_usergrouprelation ugr "
        "join main_group g on ugr.group_id = g.id "
        "join main_event e on g.id = e.group_id "
        "where ugr.user_id = \"{}\"".format(id.replace("-", ""))
    )


def get_requests_for_user(id):
    return UserGroupRelation.objects.raw(
        "select r.* from main_usergrouprelation ugr "
        "join main_group g on ugr.group_id = g.id "
        "join main_request r on ugr.group_id = r.group_id "
        "where ugr.user_id = \"{0}\" or r.author_id = \"{0}\"".format(id.replace("-", ""))
    )


def get_users_for_group(id):
    return UserGroupRelation.objects.raw(
        "select main_user.* from main_usergrouprelation "
        "join main_user "
        "on main_usergrouprelation.user_id = main_user.id "
        "where group_id = \"{}\"".format(id.replace("-", ""))
    )
