import logging
import time

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
for i in range(3):
    logging.info("tempo %s: teste 1", i)
    logging.info(f"tempo {i}: teste 2\n")
    time.sleep(1)
    print(i)