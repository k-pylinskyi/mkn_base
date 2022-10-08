class ParamsBuilder:
    def __init__(self):
        self.params = {}

    @staticmethod
    def get_supplier_params(supplier_config):
        params = {
            'supplier_name': supplier_config['name'],
            'status': supplier_config['status'],
            'updated': supplier_config['updated'],
            'download_files': supplier_config['download_files'],
            'files': ParamsBuilder.parse_file_params(supplier_config)
        }
        return params

    @classmethod
    def parse_file_params(cls, supplier_config):
        files = supplier_config['files']
        files_params = []
        for file in files:
            params = {
                'file_name': lambda: file['file_name'] if 'file_name' in file else None,
                'file_type': lambda: file['file_type'] if 'file_type' in file else 'csv',
                'filepath_or_buffer': lambda: file['url'] if 'url' in file else None,
                'sep': lambda: file['sep'] if 'sep' in file else ';',
                'decimal': lambda: file['decimal'] if 'decimal' in file else '.',
                'skip_rows': lambda: file['skiprows'] if 'skiprows' in file else 0,
                'header': lambda: file['header'] if 'header' in file else 'int',
                'compression': lambda: file['compression'] if 'compression' in file else 'infer',
                'low_memory': lambda: file['low_memory'] if 'low_memory' in file else True,
                'encoding_errors': lambda: file['encoding_errors'] if 'encoding_errors' in file else 'strict',
                'encoding': lambda: file['encoding'] if 'encoding' in file else None,
                'engine': lambda: file['engine'] if 'engin' in file else None,
                'error_bad_lines': lambda: file['error_bad_lines'] if 'error_bad_lines' in file else True,
                'on_bad_lines': lambda: file['on_bad_lines'] if 'on_bad_lines' in file else None,
                'use_cols': lambda: file['use_cols'] if 'use_cols' in file else None,
                'columns': lambda: file['columns'] if 'columns' in file else {0: 'A'}
            }
            for key, value in params.items():
                params[key] = value()
            files_params.append(params)

        return files_params

    def supplier_param_builder(self, supplier):
        supplier_raw_params = supplier
        if supplier_raw_params['multiple']:
            files = supplier_raw_params['files']
            params = {}
            for file in files.items():
                proc_builder = ProcessorBuilder()
                params[file[0]] = proc_builder.params_parser(file[1])
                file_proc = FileProcessor()
                file_proc.process_file(url=file[1]["url"], params=params[file[0]])
            print(len(supplier_raw_params["files"]))
            params['name'] = supplier_raw_params['name']
            return params

        else:
            data_params = supplier_raw_params['files']['data']
            proc_builder = ProcessorBuilder()
            file_proc = FileProcessor()
            params = proc_builder.params_parser(file_params=data_params)
            file_proc.process_file(url=data_params["url"], params=params)
            params['name'] = supplier_raw_params['name']
            return params

    def params_parser(self, file_params):
        self.params_processed['file_type'] = file_params['file_type']
        if 'encoding' in file_params and not file_params['encoding']:
            self.params_processed['encoding_errors'] = 'ignore'
        else:
            self.params_processed['encoding_errors'] = 'strict'
        if 'sep' in file_params:
            self.params_processed['sep'] = file_params["sep"]
        else:
            self.params_processed['sep'] = ','
        if 'header' in file_params and not file_params['header']:
            self.params_processed['header'] = None
        else:
            self.params_processed['header'] = 'infer'
        if 'memory' in file_params and not file_params['memory']:
            self.params_processed['low_memory'] = False
        else:
            self.params_processed['low_memory'] = True
        if 'compression' in file_params:
            self.params_processed['compression'] = file_params["compression"]
        else:
            self.params_processed['compression'] = 'infer'
        if 'error_bad_lines' in file_params and not file_params['error_bad_lines']:
            self.params_processed['error_bad_lines'] = False
        else:
            self.params_processed['error_bad_lines'] = True
        if 'use_cols' in file_params:
            self.params_processed['usecols'] = file_params["use_cols"]
        else:
            self.params_processed['usecols'] = None
        if 'columns' in file_params:
            self.params_processed['columns'] = file_params["columns"]
        else:
            self.params_processed['columns'] = None
        if 'skip_rows' in file_params:
            self.params_processed['skiprows'] = file_params["skip_rows"]
        else:
            self.params_processed['skiprows'] = None
        if 'engine' in file_params:
            self.params_processed['engine'] = file_params["engine"]
        else:
            self.params_processed['engine'] = None
        if 'decimal' in file_params and file_params['decimal']:
            self.params_processed['decimal'] = ','
        else:
            self.params_processed['decimal'] = '.'
        return self.params_processed
