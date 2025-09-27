import yaml

with open('data.yml','r',encoding='utf-8') as f:
    yaml_data = yaml.safe_load(f)
    print(yaml_data)
    print(type(yaml_data))