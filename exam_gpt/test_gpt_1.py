def build_relationships(input_text):
    relationships = {}
    statements = input_text.split(". ")
    for statement in statements:
        subjects = statement.split(" says ")
        relationships[subjects[0]] = subjects[1]
    return relationships

def is_truth_teller(person, relationships):
    statement = relationships[person]
    if "lies" in statement:
        return False
    else:
        return True

def main():
    input_text = "Vina tells the truth, Helene says Vina lies. Kandi says Helene tells the truth. Jamey says Kandi lies. Ka says Jamey lies."
    relationships = build_relationships(input_text)
    ka_tells_truth = is_truth_teller("Ka", relationships)
    if ka_tells_truth:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()