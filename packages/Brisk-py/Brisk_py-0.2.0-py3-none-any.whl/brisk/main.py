from typing import Callable, Any, Optional, Union, Iterable, TypeVar, Generator, Coroutine
from json import dumps
import re
from urllib.parse import parse_qs

from .Request import Request
from .mime import MIME

response_start = dict[str, Union[str, int, Optional[Iterable[tuple[bytes, bytes]]]]]
response_body = dict[str, Union[str, Optional[bytes], Optional[bool]]]


class App:
    def __init__(self):
        self.path_map: dict[str, dict[str, dict[Callable]]] = {'*': {}, 'GET': {}, 'POST': {}}

    @staticmethod
    def parse_url(url: str) -> Iterable[tuple[Optional[str], tuple[Optional[str], Optional[str]]]]:
        if url.endswith('/'):
            url = url[0:-1]
        char = re.compile(r'([!#$&-;=?-[]_a-z~]|%[0-9a-fA-F]{2})')
        py_var = re.compile(r'[a-zA-z_][a-zA-Z0-9_]*')
        url_vars = re.compile(r'<(int|float|slug)?:(%s)>' % py_var.pattern)

        re_int = re.compile(r'[0-9]+')
        re_float = re.compile(r'[0-9]*\.[0-9]+')
        re_slug = NotImplemented

        matches = (url_vars.match(i) for i in url.split('/'))

        print(*matches)

        def items():
            print('CALLED')
            for m in matches:
                print('item', type(m))
                if m:
                    print(m.string, m.groups())
                    yield m.string, m.groups()
                else:
                    print(None)
                    yield None, (None, None)

        return items()

    def add_route(self, path: str, handler: Callable, **optional: Optional[Any]):
        func = self._on_req(handler, {'content-type': optional.get('mime', MIME.html)})
        self.path_map[optional.get('method', '*')][path] = func

    def route(self, path: str, *, mime: Optional[str] = MIME.html, method: Optional[str] = None) -> Callable[
        [Callable[[Request], str]], None]:
        def wrapper(handler: Callable[[Request], str]):
            self.add_route(path, handler, mime=mime, method=method or '*')

        return wrapper

    def get(self, path: str, *, mime: Optional[str] = MIME.html) -> Callable[[Callable[[Request], str]], None]:
        return self.route(path, mime=mime, method='GET')

    def post(self, path: str, *, mime: Optional[str] = MIME.html) -> Callable[[Callable[[Request], str]], None]:
        return self.route(path, mime=mime, method='POST')

    @staticmethod
    def make_headers(headers: dict[str, str]):
        return list(map(lambda a: (a[0].encode('utf-8'), a[1].encode('utf-8')), headers.items()))

    def _on_req(self, handler, headers: dict, *, status: Optional[int] = 200):
        async def wrapper(request):
            body = await handler(request)
            if isinstance(body, dict):
                body = dumps(body)
                head = self.make_headers(headers | {'content-type': MIME.json})

            else:
                body = str(body)
                head = self.make_headers(headers)

            return [{'type': 'http.response.start', 'status': status, 'headers': head},
                    {'type': 'http.response.body', 'body': body.encode('utf-8')}]

        return wrapper

    async def app(self, scope: dict[str], receive, send):

        _vars = Request(scope)

        method = _vars.method.upper()
        paths = self.path_map.get(method, self.path_map.get('GET', '404'))

        if _vars.method == 'POST':
            _vars.body = await _vars.__set_body__(receive)

        if _vars.path in paths.keys():
            body = paths[_vars.path]
        elif '/*' in paths.keys():
            body = paths['/*']
        else:
            body = paths.get('404')
            if not body:
                await send({'type': 'http.response.start', 'status': 404,
                            'headers': self.make_headers({'content-type': MIME.html})})
                await send({'type': 'http.response.body', 'body': b'<h1>Page Not Found</h1>'})
                return None

        req = await body(_vars)
        for r in req:
            await send(r)
