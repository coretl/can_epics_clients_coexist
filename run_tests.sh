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
