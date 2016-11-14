import scalica_pb2
import time
import hashlib

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Processor(scalica_pb2.BetaProcessorServicer):
  def ProcessPost(self, request, context):
    print 'Post from id:%s [%s]' % (request.user_id, request.text)
    digest = hashlib.sha256(request.text).hexdigest()
    return scalica_pb2.ProcessPostReply(digest=digest)

def main():
  server = scalica_pb2.beta_create_Processor_server(Processor())
  server.add_insecure_port('[::]:22222')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(1)

if __name__ == '__main__':
  main()
