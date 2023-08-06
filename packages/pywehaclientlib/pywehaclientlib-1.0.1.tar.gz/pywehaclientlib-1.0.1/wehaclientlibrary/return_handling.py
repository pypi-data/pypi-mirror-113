class ReturnHandling:

    def __init__(self, err, status_code, message, data):
        super(ReturnHandling, self).__init__()
        self.err = err
        self.status_code = status_code
        self.message = message
        self.data = data
        