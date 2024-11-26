#!/bin/bash

# GitHub API'den en son sürüm bilgilerini alın
RELEASE_INFO=$(curl -s https://api.github.com/repos/zen-browser/desktop/releases/latest)
echo $RELEASE_INFO
# Sürüm numarasını al
VERSION="$(echo "$RELEASE_INFO" | grep -oP '"tag_name": "\K[^"]+')"
VERSION="$VERSION-b"
OUTPUT="zen-browser_"$VERSION"_amd64"

rm -rf zen-browser*
rm *.deb
mkdir -p "$OUTPUT"/opt
sed -i "s/Version: .*/Version: ${VERSION}/" DEBIAN/control

# İlgili dosyanın URL'sini al
LATEST_URL=$(echo "$RELEASE_INFO" | grep -oE 'https://github.com/zen-browser/desktop/releases/download/[a-zA-Z0-9.-]+/zen\.linux-specific\.tar\.bz2')

# Sürüm ve URL'yi yazdır
if [[ -n "$VERSION" && -n "$LATEST_URL" ]]; then
    echo "Bulunan Sürüm: $VERSION"
    echo "Dosya URL'si: $LATEST_URL"

    # Dosyayı indir
    wget -O zen-browser-$VERSION.tar.bz2 "$LATEST_URL"
    echo "Zen Browser $VERSION sürümü indirildi: zen-browser-$VERSION.tar.bz2"
    

    tar -xvjf zen-browser-$VERSION.tar.bz2 -C "$OUTPUT"/opt
    rm zen-browser-$VERSION.tar.bz2
    cp -rf usr/ DEBIAN/ "$OUTPUT"
    cp -rf distribution "$OUTPUT/opt/zen"

    dpkg-deb --build zen-browser*
else
    echo "Sürüm veya URL bulunamadı!"
fi


