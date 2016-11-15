import hashlib
import random
import scalica_pb2
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

_HASHTAGS = (
  '#yodelingchamp',
  '#gangamstyle',
  '#banphp',
  '#imadeahugemistake',
  '#iloveturtles',
)

class Processor(scalica_pb2.BetaProcessorServicer):
  def ProcessPost(self, request, context):
    print 'Post from id:%s [%s]' % (request.user_id, request.text)
    digest = hashlib.sha256(request.text).hexdigest()
    augmented_text = request.text + ' ' + random.choice(_HASHTAGS)
    return scalica_pb2.ProcessPostReply(digest=digest,
                                        augmented_text=augmented_text)

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
