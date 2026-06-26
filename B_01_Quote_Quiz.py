import csv
import random
from tkinter import *
from functools import partial # to prevent unwanted windows

# helper functions go here
def retrieve_quotes():
    """
    Retrieves quotes from csv file
    :return:  list of quotes which where each list item has the
    quotes themselves, and associated movie for the answer.
    """

    # Retrieve colours from csv file and put them in a list
    file = open("movie_quotes.csv", "r")
    all_quotes = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_quotes.pop(0)

    return all_quotes

def get_quotes_list():
    """
    Choose four colours from larger list ensuring that the scores are all different.
    :return: list of colours and score to beat (median of scores)
    """

    all_quotes = retrieve_quotes()

    round_quotes = []
    correct_quote_answer = []
    fake_quote_list = []
    fake_quote_answers = []

    # loop until we have 1 quote with its correct answer
    while len(round_quotes) < 1:
        potential_quote = random.choice(all_quotes)

        if potential_quote[1] not in correct_quote_answer:
            round_quotes.append(potential_quote[0])
            correct_quote_answer.append(potential_quote[1])

    # loop until we have 4 fake answers
    while len(fake_quote_list) < 4:
        fake_quote = random.choice(all_quotes)

        # Get the score and check it's not a duplicate
        if fake_quote[1] not in correct_quote_answer and fake_quote[1] not in fake_quote_answers:
            fake_quote_list.append(fake_quote[0])
            fake_quote_answers.append(fake_quote[1])

    return round_quotes, correct_quote_answer, fake_quote_answers


class StartQuiz:
    """
    Initial Quiz Interface (asks users how many questions they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of question from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        subtitle_string = "A quiz about iconic movie quotes"

        intro_string = ("Every question you will need to choose one of five buttons, one correctly correlating to where the quote came from. "
                        "You will need to pick the right one. Are you up to the task?")

        # choose_string = " Oops - Please choose a whole number more than zero."
        choose_string = "How many questions do you want to answer?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Quote Quiz", ("Arial", 16, "bold"), None],
            [subtitle_string, ("Arial", 12), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#4D9900"]
        ]

        # Create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary.
        self.choose_label = start_label_ref[3]

        # Frame so that enry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=4)

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=20)
        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#000000", bg="#DAE8FC", text="Start", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=1, column=0)

    def check_questions(self):
        """
        Checks users have entered 1 or more questions
        """

        # Retrieve user's amount of questions
        questions_wanted = self.num_questions_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_questions_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            questions_wanted = int(questions_wanted)
            if questions_wanted > 0:
                # Invoke Play Class (and take across number of questions)
                Play(questions_wanted)
                # Hide root window (ie: hide questions choice window).
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", 10, "bold"))
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.delete(0, END)


class Play:
    """
    Interface for playing the Colour Quest Quiz
    """

    def __init__(self, how_many):

        # rounds played - start with zero
        self.correctly_answered = IntVar()

        self.round_quote_list = []
        self.all_scores_list = []
        self.correctly_answered.set(0)

        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", 12)

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Question # of #", ("Arial", 16, "bold"), None, 0],
            ["The Quote is: PLACEHOLDER", body_font, "#FFF2CC", 1],
            ["Choose one of these movies, Good luck.", body_font, "#D5E8D4", 2],
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=500, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.quote_label = play_labels_ref[1]
        self.results_label = play_labels_ref[2]

        # set up colour buttons...
        self.question_frame = Frame(self.quiz_frame)
        self.question_frame.grid(row=3)

        self.question_button_ref = []

        # create five buttons in a 2 x 2 grid
        for item in range(0, 5):
            self.question_button = Button(self.question_frame, font=body_font,
                                          text="Placeholder", width=49,
                                          command=partial(self.round_results, item))
            self.question_button.grid(row=item // 1,
                                      column=item % 1,
                                      padx=5, pady=5)

            self.question_button_ref.append(self.question_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Round", "#0057D8", self.new_round, 34, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 16, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 16, 0, 1],
            [self.quiz_frame, "End", "#990000", self.close_play, 34, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new
        # round function for the first round.
        self.new_round()

    def to_hints(self):

        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)

    def new_round(self):
        """
        Chooses four colours, works out median for score to beat. Configures
        buttons with chosen colours.
        """

        # retrieve number of rounds played, add one to it and configure heading
        questions_played = self.questions_played.get()
        questions_played += 1
        self.questions_played.set(questions_played)

        questions_wanted = self.questions_wanted.get()

        # get quote list
        self.round_quote_list = get_quotes_list()

        # retrieve items
        question_brackets = self.round_quote_list[0]
        right_answer_brackets = self.round_quote_list[1]
        wrong_answers = self.round_quote_list[2]

        # split up + remove brackets
        question = question_brackets[0]
        right_answer = right_answer_brackets[0]

        wrong_1 = wrong_answers[0]
        wrong_2 = wrong_answers[1]
        wrong_3 = wrong_answers[2]
        wrong_4 = wrong_answers[3]

        self.all_scores_list.append(right_answer)

        answer_list = [right_answer, wrong_1, wrong_2, wrong_3, wrong_4]

        random.shuffle(answer_list)

        # Update heading, and score to beat labels. "Hide" results label
        self.heading_label.config(text=f"Round {questions_played} of {questions_wanted}")
        self.quote_label.config(text=question, font=("Arial", 14, "bold"))
        self.results_label.config(text="Choose one of these movies, Good luck.", bg="#D5E8D4")

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round)
        for count, item in enumerate(self.question_button_ref):
            item.config(text=answer_list[count], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        # alternate way to get button name. Good for if buttons have been scrambled
        answer_name = self.question_button_ref[user_choice].cget('text')

        correct_answer_list = self.all_scores_list[-1]

        if answer_name == correct_answer_list:
            result_text = f"Congrats! {answer_name} was the correct answer!"
            result_bg = "#82B366"
            self.all_scores_list.append(correct_answer_list)

        else:
            result_text = f"Oops! {answer_name} was not correct. It was {correct_answer_list}."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        questions_played = self.questions_played.get()
        questions_wanted = self.questions_wanted.get()

        if questions_played == questions_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.question_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose questions) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

class DisplayHints:
    """
    Displays hints for quote quiz
    """

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("This is a quiz about quotes from famous movies "
                     "(and sometimes TV shows)\n\n"
                     "It's up to you to correctly guess where the "
                     "quote originates from. \n\n"
                     "If you are struggling, make an educated guess. "
                     "Deduction is key, characters wouldn't be saying "
                     "'May the Force be with you' in Die Hard. \n\n"
                     "Good luck and more importantly, have fun!")

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box (and enables help button)
        """
        # put help button back to normal
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartQuiz()
    root.mainloop()