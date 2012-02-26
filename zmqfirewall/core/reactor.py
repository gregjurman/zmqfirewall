# Jacked from Moksha
# Authors: Luke Macken <lmacken@redhat.com>

"""
Choses the best platform-specific Twisted reactor
"""
import sys
try:
    if 'linux' in sys.platform:
        from twisted.internet import epollreactor
        epollreactor.install()
    elif 'freebsd' in sys.platform or 'darwin' in sys.platform:
        from twisted.internet import kqreactor
        kqreactor.install()
    elif 'win' in sys.platform:
        from twisted.internet import iocpreactor
        iocpreactor.install()
except (ImportError, AssertionError): # reactor already installed
    pass
from twisted.internet import reactor
