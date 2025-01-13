import pandas as pd
import re
import csv

def clean_text(text):
    cleaned_text = re.sub(r'^\d+_|_\d+$', '', text)
    return cleaned_text
    
    return cleaned_list
def read_excel_to_dict(file_path):
    try:
        excel_data = pd.ExcelFile(file_path)
        workbook_dict = {}
        for sheet_name in excel_data.sheet_names:
            data = pd.read_excel(file_path, sheet_name=sheet_name)
            data = data.fillna(value="")
            workbook_dict[sheet_name] = data.to_dict(orient='records')  # List of dictionaries (row-wise)
        return workbook_dict
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    file_path = "test1.xlsx"
    data_dict = read_excel_to_dict(file_path)
    flatten_data = []
    field_list = []
    if data_dict:
        for doc_link_id, data in data_dict.items():
            flatten_data_item = {}
            for row in data :
                field = clean_text(str(row.pop('doc_name', None)))
                field_list.append(field)
                for item in row:
                    if item not in flatten_data_item :
                        flatten_data_item[item] = {"doc_link_id" : doc_link_id}
                    if field in flatten_data_item[item] :
                        if flatten_data_item[item][field] == "" :
                            flatten_data_item[item][field] = row[item]
                    else :
                        flatten_data_item[item][field] = row[item]
        header = [*["document_name","doc_link_id"],*list(set(field_list))]
        for item in flatten_data_item:
            item_row = {"document_name" : item}
            item_row.update(flatten_data_item[item])
            flatten_data.append(item_row)
        csv_data = [header]
        for item in flatten_data :
            row_append = [None]*len(header)
            for key in item :
                row_append[header.index(key)] = item[key]
            csv_data.append(row_append)
        with open('out.csv','w') as f :
            writer = csv.writer(f)
            writer.writerows(csv_data)
