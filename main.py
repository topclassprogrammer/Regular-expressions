import csv
import re

PATTERN = r"^(\+?[7|8])?\s?\(?(\d{3})\)?\s?[-]?(\d{,3})[-]?" \
                          r"(\d{,2})[-]?(\d{,2})(\s?)\(?([доб.]*)\s*(\d*)\)?$"
REPLACEMENT = r"+7(\2)\3-\4-\5\6\7\8"


def open_raw_file(name):
    with open(name) as f:
        rows = csv.reader(f, delimiter=',')
        return list(rows)


def get_correct_names_phones():
    correct_names_phones = []  # Создаем список для заполнения корректными ФИО
    # и номерами телефонов
    correct_names_phones.append(raw_list[0])
    for row in raw_list[1:]:
        row_res = []
        for idx, cell in enumerate(row):
            names = cell.split()
            if 0 <= idx <= 2:
                if len(names) == 3:
                    row_res.extend([names[0], names[1], names[2]])
                elif len(names) == 2:
                    row_res.extend([names[0], names[1]])
                elif len(names) == 1:
                    row_res.append(names[0])
                elif len(names) == 0 and len(row_res) < 3 and idx == 2:
                    row_res.append(cell)
            elif (3 <= idx <= 4) or idx == 6:
                row_res.append(cell)
            elif idx == 5:
                sub_res = re.sub(PATTERN, REPLACEMENT, cell)
                row_res.append(sub_res)
        correct_names_phones.append(row_res)
    return correct_names_phones


def del_repeating_rows():
    dict_ = {}  # Создаем словарь для хранения ключей вида ('Фамилия', 'Имя')
    # и их значений в виде списка из остальных данных в строке
    for row in get_correct_names_phones():
        lastname, firstname = row[:2]
        if (lastname, firstname) not in dict_:
            dict_.setdefault((lastname, firstname), row[2:])
        else:
            empty_el_idx = []
            for idx, el in enumerate(dict_[(lastname, firstname)]):
                if el == '':
                    empty_el_idx.append(idx)
                for index in empty_el_idx:
                    idx_in_dict = dict_[(lastname, firstname)].\
                        index(el, index)
                    value_in_row = row[2:][idx_in_dict]
                    if value_in_row != '':
                        del dict_[(lastname, firstname)][idx_in_dict]
                        dict_[(lastname, firstname)].insert(idx_in_dict,
                                                            value_in_row)
    return dict_


def get_list_from_dict():
    result = []  # Создаем список для хранения преобразованных данных
    # из словаря dict_ в список подготовленный для записи в csv файл
    for names, data in del_repeating_rows().items():
        res_names = []
        for el in list(names):
            res_names.append(el)
        res_data = []
        for el in data:
            res_data.append(el)
        res_names.extend(res_data)
        result.append(res_names)
    return result


def write_result(name):
    with open(name, "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=",")
        datawriter.writerows(get_list_from_dict())


if __name__ == '__main__':
    raw_list = open_raw_file("phonebook_raw.csv")
    get_correct_names_phones()
    del_repeating_rows()
    get_list_from_dict()
    write_result("phonebook.csv")
