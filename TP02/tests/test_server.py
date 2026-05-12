from sources.server import Server

TEST_DURATION = 10000.0


def test_server():
    server: Server = Server(0, 3)
    assert server.get_id() == 0

    time: float = 0.0
    assert server.is_free(time)

    while time < TEST_DURATION:
        server.start_work(time)
        assert server.get_work_end() > time
        assert not server.is_free(time)
        time = server.get_work_end()
        assert server.is_free(time)
