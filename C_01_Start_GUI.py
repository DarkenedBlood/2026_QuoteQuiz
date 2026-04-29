from tkinter import *
# from functools import partial # to prevent unwanted windows


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

        intro_string = ("Every question you will need to choose one of four buttons, one correctly correlating to where the quote came from. "
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

        # Retrieve temperature to be converted
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
        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        self.quiz_heading_label = Label(self.quiz_frame, text=f"Question 0 of {how_many}",
                                        font=("Arial", 16, "bold"))
        self.quiz_heading_label.grid(row=0)

        self.end_quiz_button = Button(self.quiz_frame, text="End Quiz",
                                      font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#990000", width=10,
                                      command=self.close_play)
        self.end_quiz_button.grid(row=1)

    def close_play(self):
        # reshow root (ie: choose questions) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartQuiz()
    root.mainloop()