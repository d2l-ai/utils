#!/bin/bash
# Install fonts to build PDf

# En

wget -O source-serif-pro.zip https://www.fontsquirrel.com/fonts/download/source-serif-pro
unzip source-serif-pro -d source-serif-pro
sudo mv source-serif-pro /usr/share/fonts/opentype/

wget -O source-sans-pro.zip https://www.fontsquirrel.com/fonts/download/source-sans-pro
unzip source-sans-pro -d source-sans-pro
sudo mv source-sans-pro /usr/share/fonts/opentype/

wget -O source-code-pro.zip https://www.fontsquirrel.com/fonts/download/source-code-pro
unzip source-code-pro -d source-code-pro
sudo mv source-code-pro /usr/share/fonts/opentype/

sudo fc-cache -f -v

# Zh
wget https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SourceHanSansSC.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifSC_SB-H.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifSC_EL-M.zip

unzip SourceHanSansSC.zip
unzip SourceHanSerifSC_EL-M.zip
unzip SourceHanSerifSC_SB-H.zip

sudo mv SourceHanSansSC SourceHanSerifSC_EL-M SourceHanSerifSC_SB-H /usr/share/fonts/opentype/
sudo fc-cache -f -v

# KO

wget https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SourceHanSansK.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifK_SB-H.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifK_EL-M.zip

unzip SourceHanSansK.zip
unzip SourceHanSerifK_EL-M.zip
unzip SourceHanSerifK_SB-H.zip

sudo mv SourceHanSansK SourceHanSerifK_EL-M SourceHanSerifK_SB-H /usr/share/fonts/opentype/
sudo fc-cache -f -v

# JA

wget https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SourceHanSansJ.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifJ_SB-H.zip
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifJ_EL-M.zip

unzip SourceHanSansJ.zip
unzip SourceHanSerifJ_EL-M.zip
unzip SourceHanSerifJ_SB-H.zip

sudo mv SourceHanSansJ SourceHanSerifJ_EL-M SourceHanSerifJ_SB-H /usr/share/fonts/opentype/
sudo fc-cache -f -v

rm Source*.zip
