import aftership
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'../config.txt'
configParser.read(configFilePath)

test = configParser.get('aftership', 'api_key')
print(test)

# create package

# delete tracking