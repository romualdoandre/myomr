rem python arya.py -i TesteScanner/ -o out.txt -e jpg -a testes/configjpg.csv -mode append -l svm.xml
rem python arya.py -i testes/ -o out.txt -e tif -a testes/config.csv -l svm.xml -mode append
rem python arya.py -i TesteScanner/ -o out.txt -e jpg -a testes/configjpgfull.csv -mode append -l svm3.xml
rem python arya.py -i TesteScanner/ -o out.txt -e jpg -a testes/configjpg.csv -mode append -l svm3.xml
rem python arya.py -i TesteScanner/ -o out.txt -e jpg -a testes/configjpgfullcropped2.csv -mode append -l svm4.xml
rem python arya.py -i TesteScanner/ -o out.txt -e jpg -a testes/configjpgfullcropped2.csv -mode append -l svm4.xml
rem python arya.py -i fpintocropped/ -o prosel20132_d1_fpinto.dat -e jpg -a testes/prosel20132.csv -mode append -l svm4.xml
rem python arya.py -i fpintocropped/ -o prosel20132_d1_fpinto.dat -e jpg -a testes/prosel20132.csv -mode append -l svmProsel20132.xml
rem python arya.py -i uefs4cropped/ -o prosel20132_d2_uefs4.dat -e jpg -a testes/prosel20132_d2.csv -mode append -l svmProsel20132.xml
rem python arya.py -i modelodeskewcropped/ -o prosel20132_d1_modelo_deskew.dat -e jpg -a testes/prosel20132_deskew2.csv -mode append -l svmProsel20132.xml
rem python arya.py -i polivalente/ -o prosel20132_d3_polivalente.dat -e jpg -a testes/prosel20132_300dpiFull.csv -mode append -l svm300dpi.xml
rem python arya.py -i gabaritos/ -o prosel20132_gabaritos.dat -e jpg -a testes/prosel20132_300dpiFull.csv -mode append -l svm300dpi.xml
rem python arya.py -i gabaritos/ -o prosel20132_gab_scale.dat -e jpg -a testes/prosel20132_300dpi.csv -mode append -l svmscale2.xml
rem python arya.py -i uefs3/ -o prosel20132_d3_uefs3.dat -e tif -a testes/prosel20132_300dpiFull.csv -mode append -l svm300dpi.xml
rem python arya.py -i uefs3_cropped/ -o prosel20132_d3_uefs3_cropped2.dat -e tif -a testes/prosel20132_300dpi_cropped2.csv -mode append -l svm300dpi.xml
python arya.py -i ead_cropped/ -o prosel20132_ead.dat -e tif -a testes/prosel20132_300dpi_cropped2.csv
