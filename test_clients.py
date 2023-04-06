import asyncio
import sys
import threading

pv = "TEST-EPICS-CLIENTS"


def check_value(value, lib):
    print(f"Got {value} using {lib}")
    assert value == 3.141, "Not right"


loop_thread = {}

def test_aioca():
    if not loop_thread:
        lp = asyncio.new_event_loop()
        th = threading.Thread(target=lp.run_forever, daemon=True, name="loop")
        th.start()
        loop_thread[lp] = th

    async def aioca_get():
        from aioca import caget

        value = await caget(pv)
        check_value(value, "aioca")

    asyncio.run_coroutine_threadsafe(aioca_get(), loop=list(loop_thread)[0]).result(timeout=1)


def test_p4p():
    from p4p.client.thread import Context

    with Context("pva") as c:
        value = c.get(pv)
        check_value(value, "p4p")


def test_pvapy():
    from pvaccess import Channel

    c = Channel(pv)
    value = c.get()
    check_value(value["value"], "pvapy")


def test_pyepics():
    from epics import caget

    value = caget(pv)
    check_value(value, "pyepics")
    

def test_epicscorelibs():
    # not actually testing epicscorelibs, but setting the path for pyepics
    import epicscorelibs.path.pyepics


if __name__ == "__main__":
    for i in range(5):
        for cmd in sys.argv[1:]:
            globals()[f"test_{cmd}"]()
