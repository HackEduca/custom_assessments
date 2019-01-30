#!/bin/bash

#Run with ./run_unit2gen.sh [studioURL] [dynamic folder path] [template folder path]

cp -a "$3/." $2

#Go into timestamp folder
cd $2

#Change permissions on all python scripts
chmod +x unit2QuestionGenerator.py
chmod +x html_gen.py
chmod +x fetch_svg.py

#Run question generator
python unit2QuestionGenerator.py $1

#Read csv of students
IFS=","
while read f1 f2
do
        #Delete unnecessary files
        rm "$f1".json
        rm "$f1"_jsonString.txt
        
        #Generate html files for custom scripts
        python html_gen.py "$f1"_custom.txt

        #Generate svg from html files
        python fetch_svg.py q3_script0
        python fetch_svg.py q3_script1
        python fetch_svg.py q3_script2
        python fetch_svg.py q3_script3
        python fetch_svg.py q6_script0
        python fetch_svg.py q7_script0

        #convert svgs to pngs
        for file in *.svg; do inkscape $PWD/$file -e $PWD/${file%svg}png; done
        
        #Make a new directory for 
        mkdir "$f1"_images
        mv *.png "$f1"_images
        
        #Generate pdfs
        pdflatex "$f1"_test.tex

        #Delete unncessary generated files
        rm "$f1"_custom.txt
        rm *.svg
        rm *.html

done < students.csv

#Get rid of extra files
rm *.aux
rm *.log
rm -rf *_images

#Merge all the pdfs
pdfunite *.pdf "$2".pdf

#Get rid of all pdfs
rm *_test.tex
rm *_test.pdf
rm *.txt
rm *.py
rm -rf images
