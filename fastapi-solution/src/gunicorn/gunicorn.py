bind = '0.0.0.0:8000'

workers = 4
threads = 4
worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'debug'
accesslog = '-'  # stdout
errorlog = '-'  # stderr
