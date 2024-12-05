from validate_config import ValidateConfig
from instance_generator import InstanceGenerator
from config.config import Config
def main():
    config = Config()
    # Validate the configuration
    ValidateConfig.validate(config)
    generator = InstanceGenerator(config)
    
    try:
        # Generate the instances
        generator.generate()
        print(f"{config.numInstances} instance(s) successfully created in '{config.instancesDirectory}' directory.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
