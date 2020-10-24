from .models import *


def allContext(request):
    if request.session.has_key('user_id'):
        userObj = Account.objects.get(id=request.session['user_id'])
        totalReview = Reviews.objects.filter(user_id_id=request.session['user_id']).count()
        return {'users': userObj,'totalReviews': totalReview}
    return {'users': False, 'totalReviews': False}