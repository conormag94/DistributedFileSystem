def list_files():
    response = requests.get(FILE_SERVER).json()
    file_list = response['data']['files']
    for file in file_list:
        print(file['filename'], '\t', file['created_at'])