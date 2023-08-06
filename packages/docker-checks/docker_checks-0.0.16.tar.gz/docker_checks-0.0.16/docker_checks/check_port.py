import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkPortStatement():
    for index, line in enumerate(dockerfileContent):
        if 'EXPOSE' in line and '22' in line:
            logging.warning(' Line %s: Do not open port 22 nor include SSH unless specifically required', index+1)

def main():
    checkPortStatement()

if __name__ == "__main__":
    main()