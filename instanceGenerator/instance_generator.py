
import os
import random
from validate import is_valid

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

        if not os.path.isdir(instancesDirectory):
            os.makedirs(instancesDirectory)

        for i in range(numInstances):
            N = random.randint(minMembers, maxMembers)
            D = random.randint(minDepartments, maxDepartments)
            # sum of n should be less than or equal to N
            n = []
            remaining = N
            for i in range(D):
                value = random.randint(1, min(remaining, maxMembers))  # Random value, but cannot exceed remaining or maxMembers
                n.append(value)
                remaining -= value

            # If remaining > 0, you can either:
            # 1. Distribute the remaining members randomly across the departments
            # 2. Leave the remaining members as zero (or handle as needed)
            if remaining > 0:
                for i in range(remaining):
                    n[random.randint(0, D-1)] += 1  # Randomly distribute remaining members to departments


            d = [random.randint(1, D) for _ in range(N)]
            m = [[random.uniform(0, 1) if i != j else 1.0 for j in range(N)] for i in range(N)]

            instance = {
                'D': D,
                'N': N,
                'n': n,
                'd': d,
                'm': m
            }

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
