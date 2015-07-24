from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class TasksAuthorization(Authorization):

    def check_user(self,user):
        if user.is_anonymous():
            raise Unauthorized()
        else :
            return user

    def read_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return object_list.filter(user=current_user)

    def read_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return bundle.obj.user == current_user

    def create_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return object_list

    def create_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return bundle.obj.user == current_user

    def update_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        allowed = []
        for obj in object_list:
            if obj.user == current_user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return bundle.obj.user == current_user

    def delete_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return bundle.obj.user == current_user


    def delete_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return bundle.obj.user == current_user

class UsersAuthorization(Authorization):

    def check_user(self,user):
        if user.is_anonymous():
            raise Unauthorized()
        else :
            return user

    def read_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return object_list

    def read_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return True

    def create_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return current_user.is_superuser()

    def create_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        if current_user.is_superuser():
            return True
        else:
            return bundle.obj.user == current_user

    def update_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        if current_user.is_superuser():
            return True
        else:
            return bundle.obj.user == current_user

    def delete_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        return current_user.is_superuser()


    def delete_detail(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        if current_user.is_superuser():
            return True
        else:
            return bundle.obj.user == current_user

    def update_list(self, object_list, bundle):
        current_user=self.check_user(bundle.request.user)
        if current_user.is_superuser():
            return allowed
        else:
            return []
