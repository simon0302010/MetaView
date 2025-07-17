from metaview import extra_data

for single_list in extra_data.categories_dict:
    for entry in extra_data.categories_dict[single_list]:
        if entry not in extra_data.rename_dict:
            print(entry)