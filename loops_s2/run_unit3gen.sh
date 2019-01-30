#!/bin/bash

#Run with ./run_unit3gen.sh [studioURL] [dynamic folder path] [template folder path]

cp -a "$3/." $2

#Go into timestamp folder
cd $2

#Change permissions on Question Generator
chmod +x unit3QuestionGenerator.py

#Run question generator
python unit3QuestionGenerator.py $1

#Read csv of students
IFS=","
while read f1 f2
do
        #Delete unnecessary files
        rm "$f1".json
        rm "$f1"_jsonString.txt
        
        #plug in picture generator here; returns svg fils


        #convert svgs to pngs
        #for file in *.svg; do inkscape $file -e ${file%svg}png; done
        
        #mkdir "$f1"_images
        #mv *.png "$f1"_images
        
        #Generate pdfs
        pdflatex "$f1"_test.tex

done < students.csv

#Get rid of extra files
rm *.aux
rm *.log
rm *_custom.txt

#Merge all the pdfs
pdfunite *.pdf all_tests.pdf

#Get rid of all pdfs
rm *_test.tex
rm *_test.pdf