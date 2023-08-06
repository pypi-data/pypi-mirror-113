from check_add import checkAddStatement
from check_from import checkValidImage, checkLatestTag
from check_healthcheck import checkHealth
from check_upgrade import checkUpgradePackage


if __name__ == "__main__":
    checkAddStatement()
    checkValidImage()
    checkLatestTag()
    checkHealth()
    checkUpgradePackage()