class SQLGen:
    def __init__(self):
        self.new_line = '\n'
        self.file_join = ''

    def insert_data(self, id, manufacturer, supplier_part_number, part_number, qty, files, price, weight, part_name, foreign_key, inner_key):
        for file in files:
            self.file_join += f"INNER JOIN {file['name']} ON {file[foreign_key]} = {inner_key}{self.new_line}"
        self.sql_template = f'''
        SELECT
            {id} as supplier_id,
            {manufacturer},
            {supplier_part_number},
            {part_number},
            CAST(REPLACE(REPLACE({qty}), '-', '0'), '>', '') AS qty,
            {price},
            {weight},
            {part_name}
        FROM data
        {self.file_join}
        WHERE qty NOT LIKE '0'
        '''
        return self.sql_template