'''
AMMM P3 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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


