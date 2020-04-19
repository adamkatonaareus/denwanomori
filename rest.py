import log4p
import requests
import threading
import consts as CONSTS

class RestLog:

    log = None
    url = "https://areuskm.azurewebsites.net/denwa-server/rest/entry/" + CONSTS.API_KEY + "/" + str(CONSTS.DEVICE_NO) + "/"
    data = "{}"

    def __init__(self):

        logger = log4p.GetLogger(__name__, config=CONSTS.LOG4P_CONFIG)
	self.log = logger.logger

	self.log.debug("Initializing rest client...")


    def post(self, mediaId):

	try:

	    response = requests.post(self.url + mediaId, data = self.data)
	    self.log.debug("REST response status: " + str(response.status_code))

	except Exception as e:
	    log.error("Error while calling REST: " + str(e))


    def postAsync(self, mediaId):

	try:

	    postThread = threading.Thread(target=self.post, args=(mediaId,))
	    postThread.start()

	except Exception as e:
	    log.error("Error while creating POST thread: " + str(e))


