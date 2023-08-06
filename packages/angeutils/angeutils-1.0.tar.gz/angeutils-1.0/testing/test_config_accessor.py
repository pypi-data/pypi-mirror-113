# 注意：test文件的命名不要和被测试的模块文件名（即引入的模块名）一致，否则会出现无法引入错误

from angeutils.config_accessor import ConfigAccessor

from angeutils.decorators import result_checker, file_exists_checker


class ExampleConfigAccessor(ConfigAccessor):
    def __init__(self, file_path, sectioname):
        super().__init__(file_path=file_path, section_name=sectioname)

    def get_dbname(self):
        key = 'database_name'
        return self.get_str_option_value(key=key)

    def set_dbname(self, new_db_name):
        ### 注意：此处建议不写日志，在调用的上层撰写日志
        key = 'database_name'
        return self.set_str_option_value(key, new_db_name)


config_path = 'test_data\\test_config.cfg'
sectioname = 'database'

config_accessor = ExampleConfigAccessor(config_path, sectioname)


@file_exists_checker
def check_config_file():
    return config_path


@result_checker
def test_get_dbname():
    dbname = 'db_system'
    return config_accessor.get_dbname(), dbname


if __name__ == '__main__':
    test_get_dbname()

    print('finished')