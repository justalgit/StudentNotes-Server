from main.models import UserGroupRelation


def get_groups_for_user(id):
    return UserGroupRelation.objects.raw(
        "select main_group.* from main_usergrouprelation "
        "join main_group "
        "on main_usergrouprelation.group_id = main_group.id "
        "where user_id = \"{}\"".format(id.replace("-", ""))
    )


def get_users_for_group(id):
    return UserGroupRelation.objects.raw(
        "select main_user.* from main_usergrouprelation "
        "join main_user "
        "on main_usergrouprelation.user_id = main_user.id "
        "where group_id = \"{}\"".format(id.replace("-", ""))
    )
