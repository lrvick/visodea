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
from django.db import models

class Rating(models.Model):
    """ 
    This holds the rating value for whichever key you assign.

    Note, instead of using the database to compute the average, since we want to
    work on Google App Engine, update the counters as an event is added.

    Always use the following to get the Rating object:
       rating, created = Rating.objects.get_or_create(key=key)

    """

    key = models.CharField(verbose_name='Rating Key', max_length=255, unique=True)
    total_rating = models.IntegerField(verbose_name='Total Rating Sum (computed)', default=0)
    total_votes = models.IntegerField(verbose_name='Total Votes (computed)', default=0)
    avg_rating = models.FloatField(verbose_name='Average Rating (computed)', default=0.0)
    percent = models.FloatField(verbose_name='Percent Fill (computed)', default=0.0)

    def __unicode__(self):
        """ Used to identify the object in admin forms. """
        return self.key

    def add_rating(self, event):
        """
        Adds the given RatingEvent to the key.
        The event will tell you if you need to revise the counter values because 
        the user is updating their vote versus adding a new vote.

        After calling add_rating the caller should save the rating but it is 
        important the caller do the following three steps in a transaction, otherwise
        a race condition could occur:

        1. get the Rating object
        2. rating.add_rating(event)
        3. rating.save()

        """
        if event.is_changing:
            # the user decided to change their vote, so take away the old value first
            self.total_rating = self.total_rating - event.old_value
            self.total_votes = self.total_votes - 1

        self.total_rating = self.total_rating + event.value
        self.total_votes = self.total_votes + 1
        
        self.avg_rating = float(self.total_rating) / float(self.total_votes) / 20.0
        self.percent = float(self.avg_rating/5.0)

class RatingEvent(models.Model):
    """
    Each time someone votes, the vote will be recorded by ip address.
    Yes, this is not optimal for proxies, but good enough because if you
    are behind a proxy you should be working, and not rating stuff.
    """
    key = models.CharField(verbose_name='Rating Key', max_length=255)
    ip = models.IPAddressField()
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        """ A vote is from one ip address - and then it can be changed. """
        super(RatingEvent, self).__init__(*args, **kwargs)

        self.is_changing = False

    
    def __unicode__(self):
        """ Used to identify the object in admin forms. """
        return self.key + "_" + str(self.ip)
    
