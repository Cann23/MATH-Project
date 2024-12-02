from AMMMMGlobals import *

class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                      'minDepartments', 'maxDepartments', 'minMembers', 'maxMembers']
        for paramName in paramList:
            if not hasattr(data, paramName):
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))


        minDepartments = data.minDepartments
        if not isinstance(minDepartments, int) or (minDepartments <= 0):
            raise AMMMException('minDepartments(%s) has to be a positive integer value.' % str(minDepartments))

        maxDepartments = data.maxDepartments
        if not isinstance(maxDepartments, int) or (maxDepartments <= 0):
            raise AMMMException('maxDepartments(%s) has to be a positive integer value.' % str(maxDepartments))

        minMembers = data.minMembers
        if not isinstance(minMembers, int) or (minMembers <= 0):
            raise AMMMException('minMembers(%s) has to be a positive integer value.' % str(minMembers))

        maxMembers = data.maxMembers
        if not isinstance(maxMembers, int) or (maxMembers <= 0):
            raise AMMMException('maxMembers(%s) has to be a positive integer value.' % str(maxMembers))

        if maxDepartments < minDepartments:
            raise AMMMException('maxDepartments(%s) has to be >= minDepartments(%s).' % (str(maxDepartments), str(minDepartments)))


        if maxMembers < minMembers:
            raise AMMMException('maxMembers(%s) has to be >= minMembers(%s).' % (str(maxMembers), str(minMembers)))


