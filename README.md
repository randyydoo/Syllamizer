# Syllabus Simplified
**Shortens multiple syllabus documents into a single page through a trained T5 Summarization Model and the TextRank algorithm**

## Process
1. Script takes in syllabus files asking for file names
2. pdf2docx converts a pdf file to a docx to allow parsing
3. Parsing algorithm searches for key words such as "Late Policy" and "Grading Standards" 
4. Tokenize keywords and text through NLTK library
5. Utilize Text-Rank Algorithm to check for highest importance in each scentence
6. Train a t-5 base summarization model using x-sum data set
7. Feed t-5 model wil top scentences from Text-Rank algorithm to perform generative text summarization
8. Feed t-5 model's output into OpenAI API to check for grammatical mistakes


## Results
![docIMG](https://github.com/randyydoo/Syllamizer/blob/main/results/res.png)
![tableIMG](https://github.com/randyydoo/Syllamizer/blob/main/results/TableImg1.png)
![gif](https://github.com/randyydoo/Syllamizer/blob/main/results/results.gif)
