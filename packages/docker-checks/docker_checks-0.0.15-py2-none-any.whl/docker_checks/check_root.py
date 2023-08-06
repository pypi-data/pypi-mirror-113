import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkRootUser():
    for index, line in enumerate(dockerfileContent):
        if ('USER' in line and '0' in line) or ('USER' in line and 'ROOT' in line) or ('USER' in line and 'root' in line):
            logging.warning(' Line %s: User should not be specified as root', index+1)

def main():
    checkRootUser()

if __name__ == "__main__":
    main()