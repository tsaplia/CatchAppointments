import requests

FS_URL = "http://localhost:8191/v1"
headers = {
    "Content-Type": "application/json",
}


def _request(data):
    try:
        resp = requests.post(FS_URL, headers=headers, data=data).json()
    except Exception:
        raise Exception("Couldn't connect to FlareSolver")
    if resp['status'] != "ok":
        raise Exception(resp['message'])
    return resp


class FSSession:
    id = None

    def __init__(self):
        data = '{"cmd": "sessions.create"}'
        self.id = _request(data)['session']

    def __del__(self):
        if self.id is None:
            return
        data = f'{{"cmd": "sessions.destroy", "session": "{self.id}"}}'
        _request(data)

    def get(self, url):
        data = f'{{"cmd": "request.get","url": "{url}", "session": "{self.id}"}}'
        return _request(data)['solution']

    def post(self, url, post_data):
        data_list = "&".join(f'{k}={v}' for k, v in post_data.items())
        data = f'{{"cmd": "request.post","url": "{url}", "session": "{self.id}", "postData":"{data_list}"}}'
        return _request(data)['solution']
