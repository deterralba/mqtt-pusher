#!/usr/bin/python

from __future__ import (unicode_literals, absolute_import, division, print_function)

from random import randint
from math import sin

METRIC_PREFIXE = 'iot.poc.'
HOSTS = ['batman', 'snoopy', 'snoopdog', 'milou', 'superman']

class Sensor(object):
    def __init__(self, metric='indefined', tags={}):
        self.metric = METRIC_PREFIXE + metric
        self.tags = tags
        self.tags['host'] = HOSTS[randint(0, len(HOSTS)-1)]

    def get_value(self):
        raise ValueError('You must implement the get_value methode')


class Temperature(Sensor):
    def __init__(self, climate='hot', metric='temperature', **kwargs):
        Sensor.__init__(self, metric=metric, **kwargs)
        self.climate = climate

    def get_value(self):
        if self.climate == 'hot':
            _range = [70, 80]
        else:
            _range = [40, 50]
        return randint(*_range)


class Pressure(Sensor):
    def __init__(self, metric='pressure', **kwargs):
        Sensor.__init__(self, metric=metric, **kwargs)
        self.base = randint(990, 1020)

    def get_value(self):
        return self.base + randint(-5, 5)


class Light(Sensor):
    def __init__(self, metric='light', period=50, **kwargs):
        Sensor.__init__(self, metric=metric, **kwargs)
        self.period = period
        self.count = 0

    def get_value(self):
        self.count += 1
        if self.count > self.period:
            self.count = 0
        return 0.5 + 0.45*sin(self.count*2*3.14/self.period) + randint(-5, 5)/100

def get_payload(sensor):

    tags = []
    for k, v in sensor.tags.iteritems():
        if v:
            tags.append('{}:{}'.format(k, v))
        else:
            tags.append(str(k))
    return '{}:{}|g|#{}'.format(sensor.metric, sensor.get_value(), ','.join(tags))

if __name__ == '__main__':
    # t = Temperature()
    # p = Pressure()
    # l = Light()
    # sensors = [t, p, l]
    sensors = [Temperature, Pressure, Light]
    for s in [sensors[randint(0, 2)](tags={'test':'', 'cool?':'cool'}) for i in xrange(200)]:
        print(type(s).__name__, get_payload(s))
        # print([s.get_value() for i in xrange(5)])



