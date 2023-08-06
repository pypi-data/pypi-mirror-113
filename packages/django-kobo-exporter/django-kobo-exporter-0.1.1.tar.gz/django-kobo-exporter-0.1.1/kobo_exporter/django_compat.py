from django import VERSION as DJANGOVERSION

if DJANGOVERSION[0:3] < (1, 8, 0):  # pragma: no cover
    from django.conf.urls import patterns
else:

    def patterns(dummy, *args):
        return list(args)
