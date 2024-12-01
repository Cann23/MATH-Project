from instance_generator import InstanceGenerator
from config.config import Config
def main():
    config = Config()
    generator = InstanceGenerator(config)
    
    try:
        generator.generate()
        print(f"{config.numInstances} instance başarıyla '{config.instancesDirectory}' dizinine oluşturuldu.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == '__main__':
    main()
