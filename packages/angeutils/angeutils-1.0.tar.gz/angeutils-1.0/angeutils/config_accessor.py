import configparser

CONFIG_SAVE_OK = {
    'str': 'Configuration saved successfully!',
    'code': 1
}
CONFIG_SAVE_FAIL  ={
    'str': 'Configuration save failed!',
    'code': 0
}


class ConfigAccessor:
    _config_filepath = None
    _cfg_parser = configparser.ConfigParser()
    _local_section_name = None

    def __init__(self, file_path, section_name):
        self._config_filepath = file_path
        self._cfg_parser.read(self._config_filepath, encoding='utf-8')
        self._local_section_name = section_name

    def get_sections(self):
        return self._cfg_parser.sections()

    def get_str_option_value(self, key):
        '''
        :param key:
        :return: str
        '''
        return self._cfg_parser.get(self._local_section_name, key)

    def get_int_option_value(self, key):
        '''
        :param key:
        :return: int
        '''
        return self._cfg_parser.getint(self._local_section_name, key)

    def get_boolean_option_value(self, key):
        '''
        :param key:
        :return: boolean
        '''
        return self._cfg_parser.getboolean(self._local_section_name, key)

    def get_float_option_value(self, key):
        '''
        :param key:
        :return: float
        '''
        return self._cfg_parser.getfloat(self._local_section_name, key)

    def set_str_option_value(self, key, new_value):
        '''
        注：此处未写日志，须在上层调用的地方写；
        :param key:
        :param new_value:
        :return: status_code: CONFIG_SAVE_OK / CONFIG_SAVE_FAIL,
        exception_info: None / str
        '''
        try:
            self._cfg_parser.set(self._local_section_name, option=key, value=new_value)
            self._cfg_parser.write(open(self._config_filepath, 'w'))
            return CONFIG_SAVE_OK, None
        except BaseException as e:
            return CONFIG_SAVE_FAIL, str(e)

    def set_int_option_value(self, key, new_value):
        '''
        注：此处未写日志，须在上层调用的地方写；
        :param key:
        :param new_value:
        :return: status_code: CONFIG_SAVE_OK / CONFIG_SAVE_FAIL,
        exception_info: None / str
        '''
        value = str(new_value)
        return self.set_str_option_value(key=key, new_value=value)

    def set_float_option_value(self, key, new_value):
        '''
        注：此处未写日志，须在上层调用的地方写；
        :param key:
        :param new_value:
        :return: status_code: CONFIG_SAVE_OK / CONFIG_SAVE_FAIL,
        exception_info: None / str
        '''
        value = str(new_value)
        return self.set_str_option_value(key=key, new_value=value)



