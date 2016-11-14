import sys
import processor

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print 'Usage: %s <user_id> <post_id> <text>' % sys.argv[0]
    sys.exit(-1)
  print processor.process_post(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
