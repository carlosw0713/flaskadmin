taosinfoyamlpath=f"{os.path.join(BASE_DIR,'public','SQL','shiheng','taosinfo.yaml')}"
taosinfo1=YamlWay().get_yaml_data(yaml_file=taosinfoyamlpath)
taosinfo=taosinfo1.get('test')
print(f'读取taos信息:{taosinfo}')