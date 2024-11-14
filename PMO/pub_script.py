from oop import *

def main():
    pub = PMO("localhost",49002,'room')
    pub.publisher_frame()

if __name__ == "__main__":
    main()