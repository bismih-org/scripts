import os
import subprocess
import shutil
import urllib.request
import re


class Build:
    def __init__(self):
        #4:5.27.5-2+deb12u2
        self.version = "4:5.27.5-2+deb12u2-bismih"
        self.output_dir = "plasma-workspace-data_" + self.version + "_amd64"
        self.deb_file = "plasma-workspace-data_" + self.version + "_amd64.deb"

    def edit_version(self):
        file = self.output_dir + "/DEBIAN/control"
        with open(file, "r") as f:
            data = f.read()

        # Version satırını değiştirme
        new_data = re.sub(r"(?<=^Version: ).*", self.version, data, flags=re.MULTILINE)

        # Standards-Version satırını değiştirme
        new_data = re.sub(
            r"(?<=^Standards-Version: ).*", self.version, new_data, flags=re.MULTILINE
        )
        with open(file, "w") as f:
            f.write(new_data)
        print(f"Version: {self.version}")

    def download_file(self, url, dest):
        """Download the file"""
        urllib.request.urlretrieve(url, dest)
        print(f"File downloaded: {dest}")

    def extract_deb(self, deb_file):
        """.deb dosyasını çıkar"""
        os.makedirs(self.output_dir, exist_ok=True)
        subprocess.run(["dpkg-deb", "-x", deb_file, self.output_dir], check=True)
        subprocess.run(
            ["dpkg-deb", "-e", deb_file, os.path.join(self.output_dir, "DEBIAN")],
            check=True,
        )
        print(f".deb file extracted: {self.output_dir}")

    def repack_deb(self):
        """.deb dosyasını yeniden paketle"""
        subprocess.run(["dpkg-deb", "-b", self.output_dir, self.deb_file], check=True)
        print(f"Yeni .deb dosyası oluşturuldu: {self.deb_file}")

    def customize_package(self):
        r = self.output_dir + "/usr/share/plasma/look-and-feel/"
        b = r + "org.kde.breeze.desktop/contents/"
        bl = r + "org.kde.breezedark.desktop/contents/"
        bd = r + "org.kde.breezetwilight.desktop/contents/"

        shutil.copyfile("files/defaults", b + "defaults")
        shutil.copyfile("files/defaults", bl + "defaults")
        shutil.copyfile("files/defaults", bd + "defaults")

    def build(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)
        deb_url = "https://depo.pardus.org.tr/pardus/pool/main/p/plasma-workspace/plasma-workspace-data_5.27.5-2+deb12u2_all.deb"
        self.download_file(deb_url, deb_url.split("/")[-1])
        self.extract_deb(deb_url.split("/")[-1])
        subprocess.run(["rm", "-rf", "*.deb"], check=True)
        self.customize_package()
        self.edit_version()
        self.repack_deb()


if __name__ == "__main__":
    build = Build()
    build.build()
