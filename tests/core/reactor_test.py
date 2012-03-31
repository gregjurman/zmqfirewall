import mock

from nose.plugins.skip import Skip, SkipTest
from nose.tools import eq_

import sys

real_platform = str(sys.platform)

####### EPollReactor Test Install ###########

_epoll_installed = None

def _mocked_epoll_install():
    global _epoll_installed
    _epoll_installed = "epoll"

@mock.patch('sys.platform', new='linux')
def test_epoll_reactor_install():
    global _epoll_installed, real_platform
    if 'linux' in real_platform:
        with mock.patch('twisted.internet.epollreactor.install', new=_mocked_epoll_install):
            import zmqfirewall.core.reactor
    else:
        # Abort wrong platform
        raise SkipTest

    eq_(_epoll_installed, 'epoll')



####### KQReactor Test install ##############

_kq_installed = None

def _mocked_kq_install():
    global _kq_installed
    _kq_installed = "kq"

@mock.patch('sys.platform', new='freebsd')
def test_kq_reactor_install():
    global _kq_installed, real_platform
    if 'freebsd' in real_platform or 'darwin' in real_platform:
        with mock.patch('twisted.internet.kqreactor.install', new=_mocked_kq_install):
            import zmqfirewall.core.reactor
    else:
        # Abort, wrong platform
        raise SkipTest

    eq_(_kq_installed, 'kq')


####### IOCPReactor Test install ##############

_iocp_installed = None

def _mocked_iocp_install():
    global _iocp_installed
    _iocp_installed = "iocp"

@mock.patch('sys.platform', new='win32')
def test_iocp_reactor_install():
    global _iocp_installed, real_platform
    if 'win' in real_platform:
        with mock.patch('twisted.internet.iocpreactor.install', new=_mocked_iocp_install):
            import zmqfirewall.core.reactor
    else:
        # Abort, wrong platform
        raise SkipTest

    eq_(_iocp_installed, 'iocp')


def test_import_reactor():
    from zmqfirewall.core.reactor import reactor
