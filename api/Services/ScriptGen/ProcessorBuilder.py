from Services.ScriptGen.FileProcessor import FileProcessor


class ProcessorBuilder:
    def __init__(self):
        self.params_processed = {}

    def supplier_param_builder(self, supplier):
        supplier_raw_params = supplier[1]
        if supplier_raw_params['multiple'] == True:
            files = supplier_raw_params["files"]
            file_params = {}
            for file in files.items():
                proc_builder = ProcessorBuilder()
                file_params[file[0]] = proc_builder.params_parser(file[1])
                file_proc = FileProcessor()
                file_proc.process_file(url=file[1]["url"], params=file_params[file[0]])
            return file_params

        else:
            data_params = supplier_raw_params['files']['data']
            proc_builder = ProcessorBuilder()
            file_proc = FileProcessor()
            params = proc_builder.params_parser(file_params=data_params)
            file_proc.process_file(url=data_params["url"], params=params)
            return params

    def params_parser(self, file_params):
        if 'encoding' in file_params and file_params['encoding'] == False:
            self.params_processed['encoding_errors'] = 'ignore'
        else:
            self.params_processed['encoding_errors'] = 'strict'
        if 'sep' in file_params:
            self.params_processed['sep'] = file_params["sep"]
        else:
            self.params_processed['sep'] = ','
        if 'header' in file_params and file_params['header'] == False:
            self.params_processed['header'] = None
        else:
            self.params_processed['header'] = 'infer'
        if 'memory' in file_params and file_params['memory'] == False:
            self.params_processed['low_memory'] = False
        else:
            self.params_processed['low_memory'] = True
        if 'compression' in file_params:
            self.params_processed['compression'] = file_params["compression"]
        else:
            self.params_processed['compression'] = 'infer'
        if 'error_bad_lines' in file_params and file_params['error_bad_lines'] == False:
            self.params_processed['error_bad_lines'] = 'skip'
        else:
            self.params_processed['error_bad_lines'] = 'error'
        if 'use_cols' in file_params:
            self.params_processed['usecols'] = file_params["use_cols"]
        else:
            self.params_processed['usecols'] = None
        if 'skip_rows' in file_params:
            self.params_processed['skiprows'] = file_params["skip_rows"]
        else:
            self.params_processed['skiprows'] = None
        if 'engine' in file_params:
            self.params_processed['engine'] = file_params["engine"]
        else:
            self.params_processed['engine'] = None
        if 'decimal' in file_params and file_params['decimal'] == True:
            self.params_processed['decimal'] = ','
        else:
            self.params_processed['decimal'] = '.'
        return self.params_processed
