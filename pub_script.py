from oop import *

def main():
    pub = Publisher("192.168.0.112",49002,'room','hello world')
    pub.publish()

if __name__ == "__main__":
    main()