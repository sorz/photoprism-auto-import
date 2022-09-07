#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from typing import NamedTuple

import requests
from websocket import WebSocketApp


EXIT_OK = 0
EXIT_CONFIG_ERROR = 1
EXIT_REQUEST_ERROR = 2
EXIT_WEBSOCKET_ERROR = 3


class Config(NamedTuple):
    api_http: str
    api_websocket: str
    import_path: str


def get_session_id() -> str:
    cred_dir = os.environ.get('CREDENTIALS_DIRECTORY')
    if cred_dir is not None:
        cred = Path(cred_dir) / 'session_id'
        if cred.exists():
            with cred.open() as f:
                return f.read().strip()
    cred = os.environ.get('SESSION_ID')
    if cred is None:
        print('Session ID not set', file=sys.stderr)
        sys.exit(EXIT_CONFIG_ERROR)
    return cred


def get_config() -> Config:
    values = []
    missing = []
    for key in Config._fields:
        key = key.upper()
        values.append(os.environ.get(key))
        if values[-1] is None:
            missing.append(key)
    if missing:
        print(f'Missing {", ".join(missing)}.', file=sys.stderr)
        sys.exit(EXIT_CONFIG_ERROR)
    return Config(*values)


def ws_on_message(_: WebSocketApp, message: str):
    msg = json.loads(message)
    event = msg.get('event')
    # print('Event:', event)
    if event == 'import.completed':
        print('Import completed, exit.')
        sys.exit(EXIT_OK)


def ws_on_close(_: WebSocketApp, status: int, msg: str):
    print(f'WebSocket closed ({status}: {msg}), exit.', file=sys.stderr)
    sys.exit(EXIT_WEBSOCKET_ERROR)


def request_import(session_id: str, cfg: Config):
    resp = requests.post(
        f'{cfg.api_http}/import/',
        json=dict(path=cfg.import_path, move=True),
        headers={'X-Session-ID': session_id},
    )
    if not resp.ok:
        print(f'Import request failed: {resp.reason}', file=sys.stderr)
        sys.exit(EXIT_REQUEST_ERROR)
    print('Import requested, wait for finish.')


def main():
    session_id = get_session_id()
    cfg = get_config()

    def on_open(ws: WebSocketApp):
        ws.send(json.dumps(dict(session=session_id)))
        request_import(session_id, cfg)

    ws = WebSocketApp(
        url=cfg.api_websocket,
        on_open=on_open,
        on_message=ws_on_message,
        on_close=ws_on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    main()

