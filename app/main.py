import json
import os
import pprint
import sys
from packages import apkindex_to_json, get_apkindex
from schema import Response

def main():
    tar_bytes = get_apkindex()
    pkgs, pkgs_dict = apkindex_to_json(tar_bytes)


    for item in pkgs_dict:
        if item == 'python-3' or item == 'node-lts':
            print(item)
            print(pkgs_dict[item])
            content = pkgs_dict[item]
            if not os.path.exists(f"./packages/{item}"):
                os.makedirs(f"./packages/{item}")
            test = []
            for item2 in content:
                test.append(item2.model_dump(exclude_none=True))
            f = open(f"./packages/{item}/versions.json", "w")
            f.write(json.dumps(test, indent=2))
            f.close()


if __name__ == "__main__":
    main()