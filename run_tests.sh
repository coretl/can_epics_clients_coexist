# https://stackoverflow.com/a/2173421
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
python run_ioc.py &
python test_clients.py $* || (
    # It failed, but windows won't give us a coredump
    # so retry under gdb, print backtrace, then fail
    gdb python -ex "run test_clients.py $*" \
               -ex "thread apply all bt" \
               -ex "set pagination 0" \
               -ex "info proc mappings" \
               -ex "info reg" \
               -ex "disassemble" \
               -ex 'print /x * (int*) $rsp' \
               -batch
    exit 1
)
