import sys

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
            return token[0], token[2], True, token[1]
        # If standard tags match their designated level, return valid
        if token[1] in valid_tags.get(token[0]):
            return token[0], token[1], True, " ".join(token[2:])
        # Else, return invalid
        return token[0], token[1], False, " ".join(token[2:])
    else:
        # If level number invalid, return invalid
        return token[0], token[1], False, " ".join(token[2:])


def main():
    if (len(sys.argv)) != 2:
        print("Error: wrong number of arguments")
        return
    file_name = sys.argv[1]
    ged_file = open(file_name, "r")
    input_lines = ged_file.read().splitlines()
    for line in input_lines:
        print("--> {}".format(line))
        output = parse_line(line)
        print(
            "<-- {}|{}|{}|{}".format(
                output[0], output[1], "Y" if output[2] else "N", output[3]
            )
        )


if __name__ == "__main__":
    main()
