
import os
import random

class InstanceGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        minDepartments = self.config.minDepartments
        maxDepartments = self.config.maxDepartments
        minMembers = self.config.minMembers
        maxMembers = self.config.maxMembers

        #validate config

        if not os.path.isdir(instancesDirectory):
            os.makedirs(instancesDirectory)

        for i in range(numInstances):
            N = random.randint(minMembers, maxMembers)
            D = random.randint(minDepartments, maxDepartments)

            d = [random.randint(1, D) for _ in range(N)]

            d.sort()
            # find the number of members in each department
            members = [d.count(j) for j in range(1, D + 1)]

            n = [random.randint(1, members[i]) if members[i] > 0 else 0 for i in range(D)]
            m = [[random.uniform(0, 1) if k != j else 1.0 for j in range(N)] for k in range(N)]

            instance = {
                'D': D,
                'N': N,
                'n': n,
                'd': d,
                'm': m            }

            instancePath = os.path.join(instancesDirectory, f'{fileNamePrefix}_{i}.{fileNameExtension}')
            self.save_instance(instance, instancePath)
                

    def save_instance(self, instance, path):
        D, N, n, d, m = instance['D'], instance['N'], instance['n'], instance['d'], instance['m']
        with open(path, 'w') as f:
             #replace all ',' with ''
                n = str(n).replace(',', '')
                d = str(d).replace(',', '')

                # Write data to file
                f.write(f'D = {D};\n')
                f.write(f'n = {n};\n\n')
                f.write(f'N = {N};\n')
                f.write(f'd = {d};\n')

                f.write(f'm = [\n')
                for row in m:
                    newRow = str(row).replace(',', '')
                    f.write(f'    {newRow}\n')
                f.write('];\n')
