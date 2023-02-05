import api
import log

if __name__ == '__main__':
    """ API Entry point 
        Launching here 
        Shutting down by API call """

    log.information('API_LAUNCH')
    api.launching_API()
    log.information('API_SHUTDOWN')