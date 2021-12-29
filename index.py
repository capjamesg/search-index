import math
import time
import json
import os

def create_index():
    start_time = time.time()

    if os.path.isfile("index.json"):
        with open("index.json", "r") as f:
            index = json.load(f)
        number_of_documents = 0

    if os.path.isfile("word_list.json"):
        with open("word_list.json", "r") as f:
            word_list = json.load(f)
    else:
        with open("results.json", "r") as f:
            results = f.readlines()

        entries = []

        for r in results:
            try:
                r = json.loads(r.strip(","))
                entries.append(r)
            except:
                continue

        word_list = {}

        index = {}

        rolling_id = 0

        # build word list
        for e in entries:
            phrase_content = e.get("page_text").replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")
            words = phrase_content.split()
            for w in words:
                if w in word_list:
                    word_list[w.lower()] += 1
                else:
                    word_list[w.lower()] = 1

        number_of_documents = len(entries) 

        title_tree = {}

        for e in entries:
            phrase_content = e.get("page_text").replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")
            doc_title = e.get("title")

            title_as_words = doc_title.lower().split()

            # build dictionary of words

            for w in range(0, len(title_as_words)):
                if w != len(title_as_words) - 1:
                    if title_tree.get(title_as_words[w]):
                        title_tree[title_as_words[w]][title_as_words[w + 1]] = ""
                    else:
                        title_tree[title_as_words[w]] = {title_as_words[w + 1]: ""}

            doc_url = e.get("url")
            words = phrase_content.split(" ")
            incoming_links = e.get("incoming_links")

            word_checked = []

            rolling_id += 1

            word_pos = {}

            position_count = 0

            for w in words:
                if word_pos.get(w.lower()) is None:
                    word_pos[w.lower()] = [position_count]
                else:
                    word_pos[w.lower()].append(position_count)
                
                position_count += 1

            for w in words:
                if w not in word_checked and word_list.get(w.lower()) is not None:
                    tf_idf = math.log(number_of_documents / word_list[w.lower()])

                    # word_count = math.log(main_document_word_count)

                    # tf_idf = tf_idf + word_count

                    # if term appears in title, give more weight
                    if w in doc_title:
                        tf_idf = tf_idf + (doc_title.count(w) / len(doc_title) / 10)

                    if w in doc_url:
                        tf_idf = tf_idf + (doc_url.count(w) / len(doc_url) / 100)

                    if incoming_links > 0:
                        score = tf_idf + math.log(incoming_links) + math.log(len(words))
                    else:
                        score = tf_idf

                    if not index.get(w.lower()):
                        index[w.lower()] = [[rolling_id, score, word_pos.get(w.lower())]]
                    else:
                        index[w.lower()].append([rolling_id, score, word_pos.get(w.lower())])

                word_checked.append(w)

            # save all entries to text files for easy accessing
            with open("entries/{}.json".format(rolling_id), "w") as f:
                json.dump(e, f)

            print(rolling_id)

        print("built word list and index")

        for entry in index:
            index[entry] = sorted(index[entry], key=lambda x: x[1], reverse=True)

        print("ordered index")

        with open("index.json", "w+") as f:
            json.dump(index, f)

        with open("word_list.json", "w+") as f:
            json.dump(word_list, f)

        with open("title_tree.json", "w+") as f:
            json.dump(title_tree, f)

        print("saved word list and index to files")

        # order index by word frequency

        end_time = time.time()

        print("Time taken to build index: {}s".format(round(end_time - start_time, 2)))

        return index

# get all keys in nested dictionary
def get_all_keys(dictionary):
    keys = []
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            keys.extend(get_all_keys(dictionary[key]))
        else:
            keys.append(key)
    return keys

def get_autocomplete_list(word):
    word = word.lower().strip()
    with open("title_tree.json", "r") as f:
        title_tree = json.load(f)

    if title_tree.get(word):
        return get_all_keys(title_tree[word])
    else:
        return []

def search(query):
    # for i in range(0, 3):
    query = query.lower()

    candidates = {}

    candidates_by_id = {}

    if len(query.split(" ")) > 10:
        print("query too long")

    for word in range(0, len(query.split(" "))):
        w = query.split(" ")[word]

        with open("index.json", "r") as f:
            index = json.load(f)

        if index.get(w):
            ids = index[w]

            for i in ids:
                if candidates_by_id.get(w):
                    candidates_by_id[w].append(i[0])
                else:
                    candidates_by_id[w] = [i[0]]

            if candidates.get(w):
                candidates[w] += index[w]
            else:
                candidates[w] = index[w]

    in_all_entries = set.intersection(*[set(candidates_by_id[w]) for w in candidates_by_id])

    document_points = {}

    for entry in in_all_entries:
        for key, value in candidates.items():
            for e in value[:10]:
                if e[0] == entry:
                    if document_points.get(entry):
                        document_points[entry] += e[1]
                    else:
                        document_points[entry] = e[1]

    sort_entries = sorted(document_points, key=lambda x: document_points[x], reverse=True)

    rows_to_return = []

    for final_result in sort_entries[:10]:
        with open("entries/{}.json".format(final_result), "r") as f:
            entry = json.load(f)

            rows_to_return.append(entry)

    end_time = time.time()

    # print("Time: {}s".format(round(end_time - start_time, 2)))

    start_time = time.time()

    print("*" * 25)

    # print("Number of documents in index: " + str(number_of_documents))

    return rows_to_return

if __name__ == "__main__":
    create_index()