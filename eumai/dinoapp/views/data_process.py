def extract_image(data):
    images = {}
    for item in data["defect_list"]:
        images[item] = data["defect_list"][item]["images"]
    return images


def insert_construct_all_defect(inspection_data, add_data):
    inspection_data["status_waited_count"] = len(inspection_data["defect_list"])
    inspection_data["tile_count"] = 0
    inspection_data["wall_count"] = 0
    inspection_data["etc_count"] = 0
    inspection_data["remove_count"] = 0

    if len(inspection_data["defect_list"]) == len(add_data):
        for i in range(1, len(inspection_data["defect_list"])+1):
            if len(add_data[str(i)]) == 2:
                print(i)
                inspection_data["defect_list"][i]["construct_type"] = "공종"

                if add_data[str(i)][0] != "etc":
                    if add_data[str(i)][0] == "tile":
                        inspection_data["tile_count"] += 1
                    else:
                        inspection_data["wall_count"] += 1
                    inspection_data["defect_list"][i]["detail_construct_type"] = add_data[str(i)][0]
                else:
                    inspection_data["etc_count"] += 1
                    inspection_data["defect_list"][i]["detail_construct_type"] = " "

                inspection_data["defect_list"][i]["defect"] = add_data[str(i)][1] if add_data[str(i)][1] != None else " "
            else:
                inspection_data["remove_count"] += 1
                inspection_data["defect_list"][i]["construct_type"] = " "
                inspection_data["defect_list"][i]["detail_construct_type"] = " "
                inspection_data["defect_list"][i]["defect"] = " "

        return inspection_data
    else:
        return "다시 생각;;"


def insert_modified_data(inspection_data, add_data):
    inspection_data["status_waited_count"] = len(inspection_data["defect_list"])
    inspection_data["tile_count"] = 0
    inspection_data["wall_count"] = 0
    inspection_data["etc_count"] = 0
    inspection_data["remove_count"] = 0

    if len(inspection_data["defect_list"]) == len(add_data):
        for i in range(1, len(inspection_data["defect_list"])+1):
            print(add_data[str(i)])

            inspection_data["defect_list"][i]["construct_type"] = add_data[str(i)]["construct_type"]
            inspection_data["defect_list"][i]["detail_construct_type"] = add_data[str(i)]["detail_construct_type"]
            inspection_data["defect_list"][i]["defect"] = add_data[str(i)]["defect"]

        return inspection_data
    else:
        return "다시 생각;;"

def split_dict(data, piece_size):
    items = list(data.items())
    chunks = [dict(items[i:i + piece_size]) for i in range(0, len(items), piece_size)]
    return chunks


