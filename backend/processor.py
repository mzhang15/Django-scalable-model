from grpc.beta import implementations
import scalica_pb2

_TIMEOUT_SECONDS = 10

def process_post(user_id, post_id, text):
  channel = implementations.insecure_channel('localhost', 22222)
  stub = scalica_pb2.beta_create_Processor_stub(channel)
  request = scalica_pb2.ProcessPostRequest(
          user_id=user_id, post_id=post_id, text=text)
  response = stub.ProcessPost(request, _TIMEOUT_SECONDS)
  return response.digest

