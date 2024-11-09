from oop import *

def main():
    while True:
        sub = Subscriber("192.168.0.112",49002,'room')
        data = sub.subscriber()
        print(data)

if __name__ == "__main__":
    main()