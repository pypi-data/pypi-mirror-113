import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkUserSecrets():
    for index, line in enumerate(dockerfileContent):
        if ('ARG' in line) or ('ENV' in line):
            logging.warning(' Line %s: ENV and ARG should not contain any user secrets', index+1)

def main():
    checkUserSecrets()

if __name__ == "__main__":
    main()