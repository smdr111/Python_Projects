import random


class Person:
    def __init__(self):
        self.parents = [None, None]
        self.alleles = [None, None]


def create_family(generations):
    # Create a new person
    person = Person()

    # Base case: oldest generation
    if generations == 1:
        person.alleles[0] = random.choice(["A", "B", "O"])
        person.alleles[1] = random.choice(["A", "B", "O"])

    # Recursive case
    else:
        # Create parents recursively
        person.parents[0] = create_family(generations - 1)
        person.parents[1] = create_family(generations - 1)

        # Inherit one allele from each parent
        person.alleles[0] = random.choice(person.parents[0].alleles)
        person.alleles[1] = random.choice(person.parents[1].alleles)

    return person


def print_family(person, generation=0):
    if person is None:
        return

    names = ["Child", "Parent", "Grandparent"]

    print(
        "    " * generation +
        f"{names[generation]} (Generation {generation}): "
        f"blood type {''.join(person.alleles)}"
    )

    print_family(person.parents[0], generation + 1)
    print_family(person.parents[1], generation + 1)
if __name__ == "__main__":
    # Create a family with 3 generations
    family = create_family(3)
    
    # Print the family
    print_family(family)
