import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def getLineNumber(keyword):
    for index, line in enumerate(dockerfileContent):
        if keyword in line.lower():
            return index

def checkSUID():
    index = getLineNumber('from')
    if os.popen('echo $DOCKER_CONTENT_TRUST').read() == '1':
        try:
            logs = os.system('docker run ' + dockerfileContent[index].split(" ")[1] + ' find / -perm +6000 -type f').read()
            print('l->', logs)
        except: 
            logging.warning(' Line %s: the docker image is held in a private repository and hence can not be pulled', index+1)
        finally:
            if 'notary.docker.io does not have trust data' in logs:
                logging.warning(' Line %s: the docker image is not verified and hence should be used carefully', index+1)
    else:
        os.popen('export DOCKER_CONTENT_TRUST=1').read()
        try:
            logs = os.system('docker run ' + dockerfileContent[index].split(" ")[1] + ' find / -perm +6000 -type f').read()
            print('l2->', logs)
        except: 
            logging.warning(' Line %s: the docker image is held in a private repository and hence can not be pulled', index)
        finally:
            if 'notary.docker.io does not have trust data' in logs:
                logging.warning(' Line %s: the docker image is not verified and hence should be used carefully', index)
        os.popen('export DOCKER_CONTENT_TRUST=0').read()

def main():
    checkSUID()

if __name__ == "__main__":
    main()