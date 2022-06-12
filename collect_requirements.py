import os

print("\x1b[33;1mread from: requirements.txt\x1b[0m")
BASE_REQUIREMENTS = open("requirements.txt").read().split("\n")
other_requirements = BASE_REQUIREMENTS
for root, subdirs, files in os.walk("fig_dash"):
    for file in files:
        if file == "requirements.txt":
            path = os.path.join(root, file)
            print(f"\x1b[33;1mread from: {path}\x1b[0m")
            other_requirements += open(path).read().split("\n")
other_requirements = sorted(set(other_requirements), key=lambda x: x.lower())
other_requirements = sorted(other_requirements, key=lambda k: len(k))
other_requirements = "\n".join(other_requirements)
print(other_requirements)