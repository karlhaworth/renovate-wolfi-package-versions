import io
import re
import tarfile
import urllib.request as urllib2

from schema import Releases


def get_apkindex():
    response = urllib2.urlopen("https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz")
    tar_bytes = io.BytesIO(response.read())
    return tar_bytes


def apkindex_to_json(tar_bytes):
    pkgs = []
    pkgs_dict = {}

    with tarfile.open(fileobj=tar_bytes, mode="r:gz") as tar:
        for member in tar.getmembers():
            f = tar.extractfile(member)
            if "APKINDEX" in member.name and f is not None:
                content = f.read()
                pkg = {}
                for item in content.decode().split("\n"):
                    if len(item) > 0:
                        pkg[item[0]] = item[2:]
                    else:
                        # if pkg != {} and "p" in pkg and f"{package}" in pkg["p"]:
                        if pkg != {} and "p" in pkg:
                            is_lts = "-lts" if "p" in pkg and "lts" in pkg["p"] else ''

                            release = Releases(
                                    version=pkg["V"],
                                    isDeprecated=False,
                                    releaseTimestamp=pkg["t"],
                                    lts=True if "p" in pkg and "lts" in pkg["p"] else False
                                )

                            pkgs.append(
                                release
                            )
                            if ("p" in pkg and pkg["p"]) and (pkg["p"].split('=')[0].replace("cmd:", "") + f"{is_lts}" not in pkgs_dict):
                                short_pkg_name = pkg["p"].split('=')[0].replace("cmd:", "") + f"{is_lts}"
                                pkgs_dict[short_pkg_name] = []
                                print(short_pkg_name)
                                pkgs_dict[short_pkg_name].append(release)
                            elif ("p" in pkg and pkg["p"]) and (pkg["p"].split('=')[0].replace("cmd:", "") + f"{is_lts}" in pkgs_dict):
                                short_pkg_name = pkg["p"].split('=')[0].replace("cmd:", "") + f"{is_lts}"
                                print(short_pkg_name)
                                pkgs_dict[short_pkg_name].append(release)



                            pkg = {}
    return pkgs, pkgs_dict
