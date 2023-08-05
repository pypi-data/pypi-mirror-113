from urllib.parse import parse_qs


class Request:
    def __init__(self, scope: dict):
        new = self.fix(scope)

        new['headers'] = {k: v for k, v in new.get('headers')}
        print('new is', new['headers'])

        self.type: str = new.get('type')
        self.asgi: dict[str] = new.get('asgi')
        self.http_version: str = new.get('http_version')
        self.server: list[str, int] = new.get('server')
        self.client: str = new.get('client')
        self.scheme: str = new.get('scheme')
        self.method: str = new.get('method')
        self.root_path: str = new.get('root_path')
        self.path: str = new.get('path')
        self.raw_path: str = new.get('raw_path')
        self.query_string: dict[str, list[str]] = parse_qs(new.get('query_string'))
        self.headers: dict[str, str] = new.get('headers')

        if self.path.endswith('/') and len(self.path) - 1:
            self.path = self.path[0:-1]

        self.dict: dict[str] = new
        self.__dict__ = new

        self.original = scope


    def fix(self, item):
        if isinstance(item, bytes):
            return item.decode('utf-8')
        elif isinstance(item, (list, tuple)):
            return list(self.fix(i) for i in item)
        elif isinstance(item, dict):
            return {self.fix(k): self.fix(v) for k, v in item.items()}
        elif isinstance(item, (str, int, float)):
            return item
        return self.fix(list(item))

    async def __set_body__(self, rec):
        self.body: bytes = (await rec())['body']
        self.body = self.body.decode('utf-8')
        self.body = parse_qs(self.body)
        self.body = {i: self.body[i] if not len(i) - 1 else self.body[i][0] for i in self.body}

        return self.body
