import csv
import random

# Retrieve quotes from csv file and put them in a list
file = open("movie_quotes.csv", "r")
all_quotes = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_quotes.pop(0)

round_quotes = []
correct_quote_answer = []
fake_quote_list = []
fake_quote_answers = []

# loop until we have 1 quote with it's correct answer
while len(round_quotes) < 1:
    potential_quote = random.choice(all_quotes)

    # Get the score and check it's not a duplicate
    if potential_quote[1] not in correct_quote_answer:
        round_quotes.append(potential_quote[0])
        correct_quote_answer.append(potential_quote[1])

# loop until we have 4 fake answers
while len(fake_quote_list) < 4:
    fake_quote = random.choice(all_quotes)

    # Get the score and check it's not a duplicate
    if fake_quote[1] not in correct_quote_answer:
        fake_quote_list.append(fake_quote[0])
        fake_quote_answers.append(fake_quote[1])

print(f"Quote: {round_quotes}")
print(f"Right answer: {correct_quote_answer}")
print(f"Wrong answers: {fake_quote_answers}")


