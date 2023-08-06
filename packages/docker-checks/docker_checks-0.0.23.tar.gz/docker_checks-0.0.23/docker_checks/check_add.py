import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkAddStatement():
    for index, line in enumerate(dockerfileContent):
        if 'ADD' in line:
            logging.warning(' Line %s: Use COPY instead of ADD statement', index+1)

def main():
    checkAddStatement()

if __name__ == "__main__":
    main()