#
# Copyright 2008 Darrel Herbst
#
# This file is part of Django-Rabid-Ratings.
#
# Django-Rabid-Ratings is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Django-Rabid-Ratings is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Django-Rabid-Ratings.  If not, see <http://www.gnu.org/licenses/>.
#
import sys, logging
#from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import transaction
from django.db.transaction import commit_manually
#from django.http import Http404, HttpResponse, HttpResponseRedirect
from ratings.models import Rating, RatingEvent


@commit_manually
def record_vote(request):
    """ 
    Records the vote - note, we drop down and need to commit this transaction 
    manually since we need to read, compute, and then write a new value.
    This will not work with mysql ISAM tables, so if you are using mysql, it is 
    highly recommended to change this table to InnoDB to support transactions using 
    the following: 
       alter table ratings_rating engine=innodb;
    """
    result = "success"
    try:
        rating, created = Rating.objects.get_or_create(key=request.POST['id'])
        key = request.POST['id']
        ip = request.META['REMOTE_ADDR']
        event, newevent = RatingEvent.objects.get_or_create(key=key,ip=ip)
        if not newevent:
            event.is_changing = True
            event.old_value = event.value

        event.value = int(request.POST['vote'])
        rating.add_rating(event)
        rating.save()
        event.save()
        result = "%s/5 rating ( %s votes)" % (rating.avg_rating, rating.total_votes)
    except:
        transaction.rollback()
        result = 'error'
    else:
        transaction.commit()

    return HttpResponse(result)


def testview(request):
    return render_to_response('ratings/test.html')

