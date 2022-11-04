from Services.load_config import Config

class ParamsBuilder:
    @staticmethod
    def get_supplier_params(supplier_name):
        config = Config()
        supplier_config = config.get_supplier_params(supplier_name)
        params = {
            'supplier_name': supplier_name,
            'status': supplier_config['status'],
            'updated': supplier_config['updated'],
            'download_files': supplier_config['download_files'],
            'files': ParamsBuilder.parse_file_params(supplier_config),
            'sql': supplier_config.get('sql')
        }
        return params

    @classmethod
    def parse_file_params(cls, supplier_config):
        files = supplier_config['files']
        files_params = []
        for file in files:
            files_params.append({
                'file_name': file.get('file_name'),
                'file_type': file.get('file_type', 'csv'),
                'filepath_or_buffer': file.get('url'),
                'sep': file.get('sep', ';'),
                'decimal': file.get('decimal', '.'),
                'skip_rows': file.get('skip_rows', 0),
                'header': None,
                'compression': file.get('compression', 'infer'),
                'low_memory': False,
                'encoding_errors': 'ignore',
                'encoding': 'latin-1',
                #'engine': 'python',
                'on_bad_lines': 'skip',
                'use_cols': file.get('use_cols'),
                'columns': file.get('columns', {0: 'A'})
            })
        return files_params
