import os
import string
import PyPDF2
import math
import re
from math import log
from collections import Counter


def text_to_word_frequency(filepath):
    """
    Reads a text file and returns a dictionary with word frequencies.

    Args:
        filepath (str): The path to the text file.

    Returns:
        dict: A dictionary with words as keys and their frequencies as values.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            # Read the entire file content
            text = file.read()

        # Remove punctuation and convert to lowercase
        translator = str.maketrans('', '', string.punctuation + string.digits + "“" + "”" + "–" + "—" + "•" + "ü" + ""
                                   + "‐" + "" + "▪" + "―" + "‖" + "’" + "" + "€" + "‘" + "ǥ" + "" + "ʹ" + "¹" + "²"
                                   + "̶" + "­" + "δ" + "¢" + "«" + "»" + "°" + "®" + ":" + "©" + ":" + "™" + "│")
        cleaned_text = text.translate(translator).lower()

        # Split the text into words
        words = cleaned_text.split()

        # Count the frequency of each word
        word_freq = Counter(words)

        return dict(word_freq)

    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return {}
    except Exception as e:
        print(f"An error occurred with file {filepath}: {e}")
        return {}


def compute_tfidf(word_frequencies, document_frequency, total_documents):
    """
    Computes TF-IDF for a given word frequency dictionary.

    Args:
        word_frequencies (dict): Word frequency dictionary for a document.
        document_frequency (Counter): Document frequency for all words.
        total_documents (int): Total number of documents.

    Returns:
        dict: TF-IDF values for each word.
    """
    tfidf = {}
    for word, freq in word_frequencies.items():
        if word in document_frequency:
            idf = log(total_documents / document_frequency[word])
            tfidf[word] = freq * idf
    return tfidf


def process_folder(input_folder, output_folder, tfidf_output_folder):
    """
    Processes all .txt files in a folder, calculates word frequencies, saves
    the results into new .txt files, and computes a global word-document frequency.
    Also computes and saves TF-IDF values for each document.

    Args:
        input_folder (str): Path to the folder containing input .txt files.
        output_folder (str): Path to the folder where output files will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Dictionary to store document frequency (number of files containing each word)
    document_frequency = Counter()
    all_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    total_documents = len(all_files)

    # Process each .txt file in the input folder
    for filename in all_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_freq.txt")


        # Calculate word frequencies
        word_frequencies = text_to_word_frequency(input_path)

        # Update document frequency
        for word in word_frequencies.keys():
            document_frequency[word] += 1

        # Save the word frequency dictionary to a new file
        try:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for word, freq in word_frequencies.items():
                    output_file.write(f"{word}: {freq}\n")
            print(f"Processed and saved frequency: {filename}")
        except Exception as e:
            print(f"Failed to save results for {filename}: {e}")

    # Compute and save TF-IDF values
    for filename in all_files:
        input_path = os.path.join(input_folder, filename)
        tfidf_output_path = os.path.join(tfidf_output_folder, f"{os.path.splitext(filename)[0]}_tfidf.txt")

        word_frequencies = text_to_word_frequency(input_path)
        tfidf_values = compute_tfidf(word_frequencies, document_frequency, total_documents)

        try:
            with open(tfidf_output_path, 'w', encoding='utf-8') as tfidf_file:
                for word, tfidf_score in tfidf_values.items():
                    tfidf_file.write(f"{word}: {tfidf_score:.6f}\n")
            print(f"Processed and saved TF-IDF: {filename}")
        except Exception as e:
            print(f"Failed to save TF-IDF for {filename}: {e}")

    # Save the document frequency dictionary to a file
    try:
        global_output_path = os.path.join(output_folder, "global_document_frequency.txt")
        with open(global_output_path, 'w', encoding='utf-8') as global_output_file:
            for word, doc_count in document_frequency.items():
                global_output_file.write(f"{word}: {doc_count}\n")
        print("Global document frequency saved.")
    except Exception as e:
        print(f"Failed to save global document frequency: {e}")

def extract_text_from_pdf(input_folder, output_folder):
    """
    Transform pdf into txt files
    """

    all_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    for filename in all_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

        with open(input_path, 'rb') as file:
            # Read the entire file content

            reader = PyPDF2.PdfReader(file)

            pdf_text = []
            #Extract the txt for the pdf
            for page in reader.pages:
                content=page.extract_text()
                pdf_text.append(content)

            # Save the word frequency dictionary to a new file
            try:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    for line in pdf_text:
                        output_file.write(f"{line}\n")
                print(f"Processed and saved pdf to txt: {filename}")

            except Exception as e:
                print(f"Failed to save results for {filename}: {e}")


def load_tfidf_file(filepath):
    """
    Loads a TF-IDF file into a dictionary.

    Args:
        filepath (str): Path to the TF-IDF file.

    Returns:
        dict: A dictionary with words as keys and their TF-IDF values as floats.
    """
    tfidf_dict = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                word, value = line.strip().split(":")
                tfidf_dict[word.strip()] = float(value.strip())
    except Exception as e:
        print(f"Failed to load TF-IDF file {filepath}: {e}")
    return tfidf_dict

def cosine_similarity(tfidf1, tfidf2):
    """
    Calculates the cosine similarity between two TF-IDF dictionaries.

    Args:
        tfidf1 (dict): TF-IDF values for the first document.
        tfidf2 (dict): TF-IDF values for the second document.

    Returns:
        float: Cosine similarity score.
    """
    # Get the union of all words in both dictionaries
    all_words = set(tfidf1.keys()).union(set(tfidf2.keys()))

    # Compute the dot product and magnitudes
    dot_product = sum(tfidf1.get(word, 0) * tfidf2.get(word, 0) for word in all_words)
    magnitude1 = math.sqrt(sum(value ** 2 for value in tfidf1.values()))
    magnitude2 = math.sqrt(sum(value ** 2 for value in tfidf2.values()))

    # Handle cases where magnitude is zero to avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0  # No similarity if one of the vectors has no magnitude

    return dot_product / (magnitude1 * magnitude2)


def compare_tfidf_files(file1, file2):
    """
    Compares two TF-IDF files and calculates their cosine similarity score.

    Args:
        file1 (str): Path to the first TF-IDF file.
        file2 (str): Path to the second TF-IDF file.

    Returns:
        float: Cosine similarity score.
    """
    tfidf1 = load_tfidf_file(file1)
    tfidf2 = load_tfidf_file(file2)
    return cosine_similarity(tfidf1, tfidf2)

def folder_similarity_scores(input_folder, output_folder):

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "result.txt")

    # Load files
    all_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    result = {}

    for filename in range(len(all_files)):

        try:
            year = int(re.sub(r'[^\d]+', '', all_files[filename])) #Obtain the year of the file
            year2 = int(re.sub(r'[^\d]+', '', all_files[filename + 1])) #Obtain the year of the next file

            name = re.sub(r'[^\D]+', '', all_files[filename]) #Obtain the company of the file

            name2 = re.sub(r'[^\D]+', '', all_files[filename]) #Obtain the company of the next file

            if name == name2 and year == year2 - 1: # Looks if it's the same company and the years follow
                score = compare_tfidf_files(os.path.join(input_folder, all_files[filename]), os.path.join(input_folder, all_files[filename+1])) #The score is calculated

                name = name[3:] #Clean the company name
                name = name[:-9]
                name = re.sub("_", '', name)
                name = name + str(year2)
                result[name] = score
                print(f"Cosine Similarity Score of {name}: {score:.6f}")


        except Exception as e:
            print(f"Failed to process file {all_files[filename]}: {e}")

    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            for word, score in result.items():
                file.write(f"{word}: {score:.6f}\n")
        print(f"Processed and saved")
    except Exception as e:
        print(f"Failed to save : {e}")

def documents_length(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "lengths.txt")

    # Load files
    all_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    result = {}

    for filename in range(len(all_files)):

        try:
            year = int(re.sub(r'[^\d]+', '', all_files[filename]))  # Obtain the year of the file
            name = re.sub(r'[^\D]+', '', all_files[filename])  # Obtain the company of the file
            name = name[3:]  # Clean the company name
            name = name[:-9]
            name = re.sub("_", '', name)
            name = name + str(year)

            length = load_tfidf_file(os.path.join(input_folder, all_files[filename]))

            result[name] = sum(length.values())
            print(f"Length of {name}: {sum(length.values()):.6f}")

        except Exception as e:
            print(f"Failed to process file {all_files[filename]}: {e}")

    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            for word, lenght in result.items():
                file.write(f"{word}: {lenght:.6f}\n")
        print(f"Processed and saved length file")
    except Exception as e:
        print(f"Failed to save : {e}")


# Process pdf
# input_folder = "D:/Document/VSM/PDF_To_Txt/MD&A"  # Replace with the path to your input folder
# output_folder = "D:/Document/VSM/PDF_To_Txt/Output"  # Replace with the path to your output folder
#
# extract_text_from_pdf(input_folder,output_folder)

# #Process TFIDF
input_folder = "D:/Document/VSM/V2/Texts_v2/Texts/Output"  # Replace with the path to your input folder
output_folder = "D:/Document/VSM/V2/Frequence"  # Replace with the path to your output folder
tfidf_output = "D:/Document/VSM/V2/tfidf"  # Replace with the path to your output folder

process_folder(input_folder, output_folder, tfidf_output)


# #Process raw_score


input_folder = "D:/Document/VSM/V2/tfidf"  # Replace with the path to your input folder
output_folder = "D:/Document/VSM/V2/result"  # Replace with the path to your output folder

folder_similarity_scores(input_folder, output_folder)

#Process documents length

input_folder = "D:/Document/VSM/V2/Frequence"  # Replace with the path to your input folder
output_folder = "D:/Document/VSM/V2/result"  # Replace with the path to your output folder

documents_length(input_folder, output_folder)
