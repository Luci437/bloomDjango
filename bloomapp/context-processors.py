from .models import *


def allContext(request):
    if request.session.has_key('user_id'):
        userObj = Account.objects.get(id=request.session['user_id'])
        return {'users': userObj}
    return {'users': ''}