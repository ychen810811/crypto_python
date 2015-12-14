import random

msg = list('123456abcde')

def swap_str(msg):
    random.shuffle(msg)
    print('In swap_str(),\tmsg = %s' % (msg))

def main():
    random.seed()
    print('In main(),\tmsg = %s' % (msg))
    swap_str(msg)
    print('In main(),\tmsg = %s' % (msg))
 
if __name__ == '__main__':
    main()
