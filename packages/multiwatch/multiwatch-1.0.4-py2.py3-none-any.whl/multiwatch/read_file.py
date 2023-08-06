import fcntl
import os
import selectors


def read_file(file, exit_event, action, timeout=0.1):
    # Near exact copy of https://stackoverflow.com/a/49192784/240613
    # Also see https://blog.pelicandd.com/article/191
    orig_fl = fcntl.fcntl(file, fcntl.F_GETFL)
    fcntl.fcntl(file, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

    def read_line(f):
        lines = f.readlines()
        if lines:
            for line in lines:
                action(line.strip())

    selector = selectors.DefaultSelector()
    selector.register(file, selectors.EVENT_READ, read_line)

    while not exit_event.is_set():
        for k, mask in selector.select(timeout):
            callback = k.data
            callback(k.fileobj)


def read_file_into_queue(file, exit_event, queue, transform=None, timeout=0.1):
    """
    Processes the lines from a file in a loop, putting them in a queue as they
    arrive. The method can be used to read from `stdin`, or from an arbitrary
    file.
    """
    def action(line):
        processed = transform(line) if transform else line
        queue.put(processed)

    read_file(file, exit_event, action, timeout=0.1)
