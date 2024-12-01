from validate_config import ValidateConfig
from instance_generator import InstanceGenerator
from config.config import Config
def main():
    config = Config()
    ValidateConfig.validate(config)
    generator = InstanceGenerator(config)
    
    try:
        generator.generate()
        print(f"{config.numInstances} instance başarıyla '{config.instancesDirectory}' dizinine oluşturuldu.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
