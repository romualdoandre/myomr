python align.py 40 130 2360 3380 test/*.png
python crop.py 40 130 2360 3380 test/rot*
python omr.py -i test/crop_rot* -o output.dat -a test.csv -t 100