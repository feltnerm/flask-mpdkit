from flask import _request_ctx_stack
from mpd import MPDClient, MPDError, CommandError

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

ctx_stack = stack


class MPD(MPDClient):

    def __init__(self, host='localhost', port=6600, use_unicode=True, *args, **kwargs):
        self._host = host
        self._port = port
        self.use_unicode = use_unicode
        self._connected = False
        super(MPD, self).__init__(use_unicode=use_unicode,
                *args, **kwargs)
        self.connect()

    def connect(self):
        try:
            super(MPD, self).connect(self._host, self._port)
            self._connected = True
        except IOError as (errno, strerror):
            raise Exception("Could not connect to '%s': %s" % (self._host,
             strerror))

    def disconnect(self):
        try:
            super(MPD, self).close()
        except (MPDError, IOError) as e:
            pass

        try:
            super(MPD, self).disconnect()
            self._connected = False
        except (MPDError, IOError):
            print 'Something is seriously broken.'
            super(MPD, self).__init__(use_unicode=self.use_unicode)

    @staticmethod
    def __getattr__(self, name):
        if hasattr(MPDClient, name):
            return getattr(MPDClient, name)


class MPDKit(object):

    def __init__(self, app=None, *args, **kwargs):

        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app, *args, **kwargs):
        app.config.setdefault('MPD_HOST', 'localhost')
        app.config.setdefault('MPD_PORT', 6600)
        app.config.setdefault('MPD_CONFIG', '/etc/mpd.conf')
        app.config.setdefault('MPD_USERNAME', None)
        app.config.setdefault('MPD_PASSWORD', None)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self._teardown_request)
        elif hasattr(app, 'teardown_request'):
            app.teardown_request(self._teardown_request)
        else:
            app.after_request(self._teardown_request)

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mpd'] = self

        self.app = app

    def connect(self):

        if self.app is None:
            raise RuntimeError('The mpd extension was not init to any app')

        ctx = ctx_stack.top
        mpd_client = getattr(ctx, 'mpd_client', None)
        if mpd_client is None:
            # Connect to MPD here
            ctx.mpd_client = MPD(host=ctx.app.config.get('MPD_HOST'),
                                 port=ctx.app.config.get('MPD_PORT'))

    @property
    def is_connected(self):
        ctx = ctx_stack.top
        return getattr(ctx, 'mpd_client', None) is not None

    def disconnect(self):
        if self.is_connected:
            ctx = ctx_stack.top
            ctx.mpd_client.disconnect()
            del ctx.mpd_client

    def _teardown_request(self, response):
        self.disconnect()
        return response

    def __getattr__(self, name, *args, **kwargs):
        if not self.is_connected:
            self.connect()
        mpd_client = getattr(ctx_stack.top, 'mpd_client')
        if hasattr(mpd_client, name):
            return getattr(mpd_client, name)
        else:
            return {}
