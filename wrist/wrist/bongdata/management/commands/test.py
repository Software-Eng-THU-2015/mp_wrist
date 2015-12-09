from django.core.management.base import BaseCommand, CommandError
import tools

class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in xrange(100):
            for j in xrange(20151119, 20151203):
                tools.CreateData(i, j)
        for i in xrange(99):
            for j in xrange(20151111, 20151119):
                tools.CreateData(i+1,j)
#        tools.CreateData(0,20151201)
        print "successful!"
