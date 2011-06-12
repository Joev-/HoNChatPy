import time
import threading

shutdown_event = threading.Event()

def dowork():
  while not shutdown_event.is_set():
    time.sleep(1.0)

def main():
  """ Start some threads & stuff. """

  t = threading.Thread(target=dowork, args=(), name='worker')
  t.start()

  try:
    while t.is_alive():
      t.join(timeout=1.0)
  except (KeyboardInterrupt, SystemExit):
    shutdown_event.set()

if __name__ == '__main__':
  main()