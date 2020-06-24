def data_file_string_is_accurate(data: str):
    return all([
        data[:10] == '{"id":"248',
        data[-10:] == ':59:59Z"}\n'
    ])
