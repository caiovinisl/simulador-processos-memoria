import json

#TODO: Needs to comment code

def create_file(path:str,file_name:str)-> None:
    with open(f"{path}/{file_name}",'w') as file:
        # print("criando arquivo")
        json.dump({"1":0}, file, ensure_ascii=False, indent=4)


def write(path:str,file_name:str, cicle_id:int, cicle_data:dict)-> None:
    
    with open(f"{path}/{file_name}",'r') as file:
        # print("lendo")
        old_json = json.load(file)

    with open(f"{path}/{file_name}",'w') as file:
        # print("writing")
        # print(f"old json {old_json}")
        old_json[str(cicle_id)] = cicle_data
        json.dump(old_json, file, ensure_ascii=False, indent=4)
        

def read_cicle_id(path,file_name,cicle_id)-> dict:
    with open(f"{path}/{file_name}",'r') as file:
        print(f"lendo cicle_id = {cicle_id}")
        old_json = json.load(file)
    return old_json[str(cicle_id)]
