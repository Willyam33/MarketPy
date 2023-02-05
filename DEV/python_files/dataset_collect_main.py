import listen_to_dataset_arrival
import log

if __name__ == '__main__':

    # Launching listening on new dataset arrival
    log.information('DATASET_COLLECT_LAUNCH')
    listen_to_dataset_arrival.listening()

