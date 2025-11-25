# TF-IDF_Master_Project

List of scripts used for my master's project.
The "process PDF" function using the PyPDF2 library was abandoned, and an OCR tool was used instead due to difficulties with certain PDFs.

Note: Some comments in the code were generated with the help of ChatGPT.

---

## HOW TO USE

1. At the end of the program, change the directory paths to match the document paths for your project.

2. If you want to process PDFs (convert them into .txt files) using this program:

   * Remove the comments after the "# Process pdf" line.
   * Change the input and output paths to the correct locations for your project.
     If you already converted the PDFs to text using an OCR tool or another method, skip directly to the "# Process TFIDF" section.

3. For the "# Process pdf" section:

   * The input path must be a folder containing PDF files.
   * The output path must be an empty folder.
   * PDFs must be named using the following format:
     countryCode_Ticker_year
   * The output will consist of .txt documents.

4. Use the folder containing the .txt files as the input folder for the "# Process TFIDF" section.

5. Prepare two empty folders as output folders for the "# Process TFIDF" section:

   * One empty folder for the "Frequency" output.
   * One empty folder for the "TFIDF" output.

6. The Frequency output will consist of .txt files containing dictionaries where:

   * Keys are words found in the document.
   * Values are the number of times each word appears.
     An additional .txt file will be created containing a combined dictionary of word-count pairs across all documents.

7. The TFIDF output will contain the frequency dictionaries adjusted according to the term frequencies in all documents.

8. The "# Process raw_score" section takes the TFIDF output folder as input.
   It produces a .txt file containing a dictionary where:

   * Keys are document names.
   * Values are similarity scores for documents with consecutive years.

9. The "# Process documents length" section takes the Frequency output folder (from the "# Process TFIDF" section) as input.
   The output folder must be empty.
   This step produces a .txt document containing a dictionary where:

   * Keys are document names.
   * Values are the total word count for each document.
