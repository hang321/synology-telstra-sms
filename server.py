#!/usr/bin/env python2.7
import logging, sys, traceback
import telstrasmsapi

from urlparse import parse_qsl

logger = logging.getLogger('telstra-sms')

try:
    import config
except ImportError:
    raise RuntimeError("no config")


class BadRequest(Exception):
    pass


def send_sms_message(params, environ):
    try:
        appkey = params['appkey'].strip()
        appsecret = params['appsecret'].strip()
        number = params['to'].strip()
        message = params['text'].strip()
    except (ValueError, KeyError) as e:
        raise BadRequest("Missing/invalid parameter: %s" % e)

    logger.info('Request: appkey=%s, to=%s, message=%s'
        % (appkey, number, message))

    # Prepare some of the values
    if number[:1] == '+':
        number = number[2:]

    try:
        api = telstrasmsapi.TelstraSmsApi(appkey, appsecret)
        token = api.authenticate()
        response = api.sendMessage(token, number, message)
        logger.info('Response: %s', response)

    except Exception as e:
        logger.warn(traceback.format_exc())

    return 'ok'


def app(environ, start_response):
    """The URL we receive must look something like this:
    http://localhost:18964/?appkey=FOO&appsecret=BAR&to=12345&text=Hello+World
    See Synology help file
    """

    if environ.get('PATH_INFO', '').lstrip('/').rstrip('/') != '':
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['error 404']

    try:
        args = dict(parse_qsl(environ['QUERY_STRING']))
        response = send_sms_message(args, environ)
    except BadRequest, e:
        logger.error('Error: %s' % e)
        start_response('400 Bad Request', [('Content-type', 'text/plain')])
        return ['%s' % e]
    except Exception, e:
        logger.error('Error: %s' % e)
        raise
    else:
        logger.info('Success')
        start_response('200 Ok', [('Content-type', 'text/plain')])
        return [response]


def serve():
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', config.PORT, app)
    httpd.serve_forever()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        handler = logging.FileHandler(config.LOGFILE)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        import daemon  # doesn't work on Windows, btw.
        with daemon.DaemonContext(files_preserve=[handler.stream]):
            serve()
    else:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        serve()
