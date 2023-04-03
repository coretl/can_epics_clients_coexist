import asyncio

pv = "TEST-EPICS-CLIENTS"


def check_value(value):
    print(f"Got {value}")
    assert value == 3.141, "Not right"


async def test_ca():
    # aioca uses epicscorelibs
    from aioca import caget, purge_channel_caches

    value = await caget(pv)
    check_value(value)
    purge_channel_caches()


def test_p4p():
    # p4p uses epicscorelibs
    from p4p.client.thread import Context

    with Context("pva") as c:
        value = c.get(pv)
        check_value(value)


def test_pvapy():
    from pvaccess import Channel

    c = Channel(pv)
    value = c.get()
    check_value(value["value"])


def test_pyepics():
    from epics import caget

    value = caget(pv)
    check_value(value)    


def epicscorelibs_last_works():
    test_pyepics()
    test_pvapy()
    asyncio.run(test_ca())
    test_p4p()    

def pyepics_epicscorelibs_works():
    asyncio.run(test_ca())
    test_p4p()    
    # This import tells pyepics to use epicscorelibs version of libca
    import epicscorelibs.path.pyepics
    test_pyepics()

def pyepics_epicscorelibs_first_fails():
    import epicscorelibs.path.pyepics
    test_pyepics()
    asyncio.run(test_ca())
    test_p4p()    
    # Runs through, but fails on exit:
    # Thread 1 "python" received signal SIGSEGV, Segmentation fault.
    # 0x00007fffd9277300 in epicsMutexLock ()
    #     from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/./libCom.so.7.0.7.99.0

def pyepics_last_fails():
    asyncio.run(test_ca())
    test_p4p()    
    test_pyepics()    
    # Runs through, but fails on exit
    #0  0x00007ffff68a7aff in raise () from /lib64/libc.so.6
    #1  0x00007ffff687aea5 in abort () from /lib64/libc.so.6
    #2  0x00007ffff68ea097 in __libc_message () from /lib64/libc.so.6
    #3  0x00007ffff68f14ec in malloc_printerr () from /lib64/libc.so.6
    #4  0x00007ffff68f3354 in _int_free () from /lib64/libc.so.6
    #5  0x00007fffe4298fc5 in fdManager::~fdManager() ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/./libCom.so.7.0.7.99.0
    #6  0x00007ffff68aa29c in __run_exit_handlers () from /lib64/libc.so.6
    #7  0x00007ffff68aa3d0 in exit () from /lib64/libc.so.6
    #8  0x00007ffff6893d8c in __libc_start_main () from /lib64/libc.so.6
    #9  0x000055555555475e in _start ()

def pvapy_last_fails():
    asyncio.run(test_ca())
    test_p4p()    
    test_pvapy()
    # Gets half way through
    #0  0x00007ffff6925fd5 in __strlen_avx2 () from /lib64/libc.so.6
    #1  0x00007fffe4717621 in tcpiiu::hostNameSetRequest(epicsGuard<epicsMutex>&) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #2  0x00007fffe471ad35 in tcpiiu::tcpiiu(cac&, epicsMutex&, epicsMutex&, cacContextNotify&, double, epicsTimerQueue&, osiSockAddr const&, comBufMemoryManager&, unsigned int, ipAddrToAsciiEngine&, unsigned int const&, SearchDestTCP*) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #3  0x00007fffe46fd9c6 in cac::findOrCreateVirtCircuit(epicsGuard<epicsMutex>&, osiSockAddr const&, unsigned int, tcpiiu*&, unsigned int, SearchDestTCP*) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #4  0x00007fffe46fe9e5 in cac::transferChanToVirtCircuit(unsigned int, unsigned int, unsigned short, unsigned long, unsigned int, osiSockAddr const&, epicsTime const&) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #5  0x00007fffe4706010 in udpiiu::searchRespAction(ca_hdr const&, osiSockAddr const&, epicsTime const&) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #6  0x00007fffe470678f in udpiiu::postMsg(osiSockAddr const&, char*, unsigned long, epicsTime const&) ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #7  0x00007fffe47069c4 in udpRecvThread::run() ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/libca.so.7.0.7.99.0
    #8  0x00007fffe429ce69 in epicsThreadCallEntryPoint ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/./libCom.so.7.0.7.99.0
    #9  0x00007fffe4288d65 in start_routine ()
    #   from /dls/science/users/tmc43/repos/can_epics_clients_coexist/venv/lib64/python3.9/site-packages/epicscorelibs/lib/./libCom.so.7.0.7.99.0
    #10 0x00007ffff73b11ca in start_thread () from /lib64/libpthread.so.0
    #11 0x00007ffff6892e73 in clone () from /lib64/libc.so.6

if __name__ == "__main__":
    # Uncomment only one of the below
    for i in range(5):
        #epicscorelibs_last_works()
        #pyepics_epicscorelibs_works()
        #pyepics_epicscorelibs_first_fails()
        #pyepics_last_fails()
        #pvapy_last_fails()