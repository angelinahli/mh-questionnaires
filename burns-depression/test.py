import json
import os
from datetime import date

PATH = os.path.dirname(os.path.abspath(__file__))

ANSWER_KEY = {
    0: "Not At All",
    1: "Somewhat",
    2: "Moderately",
    3: "A Lot",
    4: "Extremely"
}

RESULTS = [
    { "lower_bound": 0, "upper_bound": 5, "meaning": "No depression" },
    { "lower_bound": 6, "upper_bound": 10, "meaning": "Normal but unhappy" },
    { "lower_bound": 11, "upper_bound": 25, "meaning": "Mild depression" },
    { "lower_bound": 26, "upper_bound": 50, "meaning": "Moderate depression" },
    { "lower_bound": 51, "upper_bound": 75, "meaning": "Severe depression" },
    { "lower_bound": 76, "upper_bound": 100, "meaning": "Extreme depression" }
]

def get_question_sections():
    # questions are a list of dictionaries of question sections
    with open(os.path.join(PATH, "questions.json"), "r") as fl:
        questions = json.loads(fl.read())
    return questions

def get_result_dict():
    result_dict = {}
    for level in RESULTS:
        for i in range(level["lower_bound"], level["upper_bound"] + 1):
            result_dict[i] = level["meaning"]
    return result_dict

def get_answer_key():
    answers = sorted(list(ANSWER_KEY.items()))
    return " | ".join(["{} - {}".format(ans, val) for ans, val in answers])

def get_rating(txt):
    str_rating = raw_input(txt).strip().decode('utf-8')
    if not str_rating.isnumeric() or int(str_rating) not in ANSWER_KEY:
        print("\nPlease answer a valid answer! Here is the answer key:")
        print(get_answer_key())
        return get_rating(txt)
    return int(str_rating)

def get_answers():
    sections = get_question_sections()
    total_rating = 0
    answers = []
    num_questions = 0
    any_suicidal = False

    print("Thanks for taking the Burns Depression Test!")
    print("Please indicate how much you have experienced each symptom during "
        + "the past week, including today. Please answer all 25 items.")
    print("\nAnswer key:")
    print(get_answer_key())

    for section in sections:
        heading = section["section_heading"]
        print("\n** " + heading + " **")
        for question in section["questions"]:
            text = "{num}. {question} ".format(
                num=num_questions + 1,
                question=question)
            rating = get_rating(text)
            answers.append([section, question, rating])
            total_rating += rating
            num_questions += 1
            if heading.lower() == "suicidal urges" and rating > 0:
                any_suicidal = True

    data = {
        "answers": answers,
        "total": total_rating,
        "result": get_result_dict()[total_rating],
        "any_suicidal": any_suicidal
    }
    return data

def save_answers(answer_data):
    now = date.today().isoformat()
    path = os.path.join(PATH, "output")
    filename = os.path.join(path, "{}.json".format(now))

    if not os.path.exists(path):
        os.makedirs(path)
    with open(filename, "w") as fl:
        fl.write(json.dumps(answer_data))

def print_answers(answer_data, print_questions=False):
    print("\n\nThanks for completing this!!")

    if answer_data["any_suicidal"]:
        print("\n*** IMPORTANT ***")
        print("You have indicated here that you are experiencing suicidal feelings.")
        print("It is advised that you seek immediate help with a mental health professional!")
        print("More information can be found at the following address:")
        print("https://suicidepreventionlifeline.org/")
        print("*****************")

    print("\nTotal score: {}".format(answer_data["total"]))
    print("Interpretation of score: {}".format(answer_data["result"]))

    if print_questions:
        for section, question, rating in answer_data["answers"]:
            print("{} / {} - {}".format(section, question, rating))

def run(filename=None):
    if not filename:
        answer_data = get_answers()
        save_answers(answer_data)
        print_answers(answer_data)
    else:
        with open(filename, "r") as fl:
            answer_data = json.loads(fl.read())
        print_answers(answer_data, print_questions=True)

if __name__ == "__main__":
    run()
