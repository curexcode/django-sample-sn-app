from django.db import models
from account.models import Account


class Connection (models.Model):
    user = models.ManyToManyField(Account) 
    current_user = models.ForeignKey(Account, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def add_connection(cls, current_user, new_connection):
        current_user_id = Account.objects.get(pk=current_user)
        connection, created = cls.objects.get_or_create(current_user=current_user_id)
        connection.user.add(new_connection)

    @classmethod
    def remove_connection(cls, current_user, old_connection):
        current_user_id = Account.objects.get(pk=current_user)
        connection, created = cls.objects.get_or_create(current_user=current_user_id)
        connection.user.remove(old_connection)

    @classmethod    
    def get_connection(cls, current_user):
        '''
        Gives you list of all connections of given user ID.
        '''
        connection = cls.objects.get(current_user_id=current_user)
        # import pdb; pdb.set_trace()
        users = connection.user.all()
        return users
    
    @classmethod
    def is_connection(cls, current_user, user):
        '''
            This function returns true if user1 is connection of user2
        '''
        try:
            connection = cls.objects.get(current_user_id=current_user)
            connections = connection.user.all()
        except:
            return False
        # c1 = cns[0]
        user_account = Account.objects.get(pk=user)
        return user_account in connections
