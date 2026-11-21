import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from bokeh.client import pull_session

VIZ_SCRIPT = (
    Path(__file__).resolve().parent.parent / "src" / "trig_visualisation" / "viz.py"
)
STARTUP_TIMEOUT_SECONDS = 60


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
def bokeh_server():
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "bokeh", "serve", str(VIZ_SCRIPT), "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    base_url = f"http://127.0.0.1:{port}/viz"
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if server.poll() is not None:
            pytest.fail(f"bokeh serve exited early:\n{server.stdout.read()}")
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1).close()
            break
        except OSError:
            time.sleep(0.5)
    else:
        server.kill()
        pytest.fail("bokeh serve did not start listening in time")
    yield base_url
    server.terminate()
    server.wait(timeout=10)


def test_served_app_builds_the_visualisation_document(bokeh_server):
    with pull_session(url=bokeh_server) as session:
        document = session.document

        assert document.title == "Trigonometry Values"
        assert len(document.roots) == 1
