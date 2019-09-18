import sys
import json
from prettytable import PrettyTable
from collections import defaultdict

valid_tags = {
    "0": ("HEAD", "TRLR", "NOTE"),
    "1": (
        "NAME",
        "SEX",
        "BIRT",
        "DEAT",
        "FAMC",
        "FAMS",
        "MARR",
        "HUSB",
        "WIFE",
        "CHIL",
        "DIV",
    ),
    "2": ("DATE"),
}


def parse_line(raw_line):
    token = raw_line.split(" ")
    # Check validity of level number
    if token[0] in valid_tags.keys():
        # If special tags are in 3rd position, return valid
        if len(token) > 2 and token[0] == "0" and token[2] in ("INDI", "FAM"):
            return int(token[0]), token[2], True, token[1]
        # If standard tags match their designated level, return valid
        if token[1] in valid_tags.get(token[0]):
            return int(token[0]), token[1], True, " ".join(token[2:])
        # Else, return invalid
        return int(token[0]), token[1], False, " ".join(token[2:])
    else:
        # If level number invalid, return invalid
        return int(token[0]), token[1], False, " ".join(token[2:])


def convert_date(raw_date):
    return raw_date


def get_split_entries(gedcom_lines):
    uid_type = None
    uid = None
    entry = defaultdict(list)
    for line in gedcom_lines:
        level, tag, valid, args = parse_line(line)
        if valid == False or tag in ("NOTE", "TRLR", "NOTE"):
            continue
        if uid is None and uid_type is None:
            uid_type = tag
            uid = args
        if level == 0 and len(entry) != 0:
            yield uid_type, uid, dict(entry)
            uid_type = tag
            uid = args
            entry = defaultdict(list)
        else:
            if tag == "DATE":
                entry[last_tag].append(convert_date(args))
            elif len(args) != 0:
                entry[tag].append(args)
        last_tag = tag
    if len(entry) != 0:
        yield uid_type, uid, dict(entry)


def print_individuals(ind_data):
    ind_ids = sorted(ind_data.keys())
    x = PrettyTable()
    x.field_names = ["Individual ID", "Individual Name"]
    for ind_id in ind_ids:
        ind_name = ind_data[ind_id]["NAME"]
        x.add_row([ind_id, ind_name])
    print(x)


def print_families(fam_data, ind_data):
    fam_ids = sorted(fam_data.keys())
    x = PrettyTable()
    x.field_names = ["Family ID", "Husband ID", "Husband Name", "Wife ID", "Wife Name"]
    for fam_id in fam_ids:
        husb_ids = fam_data[fam_id]["HUSB"]
        wife_ids = fam_data[fam_id]["WIFE"]
        husb_name = [ind_data[uid]["NAME"] for uid in husb_ids]
        wife_name = [ind_data[uid]["NAME"] for uid in wife_ids]
        x.add_row([fam_id, husb_ids, husb_name, wife_ids, wife_name])
    print(x)


def main():
    if (len(sys.argv)) != 2:
        print("Error: wrong number of arguments")
        return
    file_name = sys.argv[1]
    ged_file = open(file_name, "r")

    # input_lines = (line for line in ged_file.read().splitlines())
    input_lines = ged_file.read().splitlines()

    individuals = {}
    families = {}

    for uid_type, uid, data in get_split_entries(input_lines):
        if uid_type == "INDI":
            individuals[uid] = data
        elif uid_type == "FAM":
            families[uid] = data
        else:
            print("Unexpected uid_type: {}".format(uid_type))

    print_individuals(individuals)
    print_families(families, individuals)

    with open("families.json", "w") as outfile:
        json.dump(families, outfile)
    with open("individuals.json", "w") as outfile:
        json.dump(individuals, outfile)

    # for line in input_lines:
    #     print("--> {}".format(line))
    #     output = parse_line(line)
    #     print(
    #         "<-- {}|{}|{}|{}".format(
    #             output[0], output[1], "Y" if output[2] else "N", output[3]
    #         )
    #     )


if __name__ == "__main__":
    main()
