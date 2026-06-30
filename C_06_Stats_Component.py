from tkinter import *
from functools import partial

class StartGame:
    """
    Initial Game Interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of round from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.play_button = Button(self.start_frame,
                                     text="Play",
                                     fg="#000000",
                                     bg="#DAE8FC",
                                     font=("Arial", 14, "bold"), width=12,
                                     command=self.check_rounds)
        self.play_button.grid(row=1, padx=5, pady=5)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of rounds to be played.
        """
        Play(num_rounds)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve wanted round amount
        rounds_wanted = 5
        self.to_play(rounds_wanted)

class Play:

    def __init__(self, how_many):

        # Excellent Test Data
        self.incorrect_list = []
        self.correct_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Mediocre Test Data
        # self.incorrect_list = [1, 1, 1, 1, 1]
        # self.correct_list = [1, 1, 1, 1, 1]

        # Awful Test Data
        # self.incorrect_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # self.correct_list = []

        self.rounds_played = len(self.incorrect_list) + len(self.correct_list)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Quote Quiz", font=("Arial", 14, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """

        # IMPORTANT: retrieve number of questions
        # won as a number (rather than the 'self' container)
        stats_bundle = [self.rounds_played, self.correct_list,
                        self.incorrect_list]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays stats from colour quest game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        rounds_played = all_stats_info[0]
        correct_list = all_stats_info[1]
        incorrect_list = all_stats_info[2]

        correct_amount = len(correct_list)
        incorrect_amount = len(incorrect_list)

        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        success_rate = correct_amount / rounds_played * 100

        # Strings for Stats labels...
        success_string = (f"Success Rate: {correct_amount} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        rounds_string = f"Rounds Played: {rounds_played}"
        correct_string = f"Questions answered correctly: {correct_amount}"
        incorrect_string = f"Questions answered incorrectly: {incorrect_amount}"

        # custom comment text and formatting
        if correct_amount == rounds_played:
            comment_string = ("Amazing! You've answered every "
                              "question correctly!")
            comment_colour = "#D5E8D4"

        elif correct_amount == 0:
            comment_string = ("Oops - You haven't answered any questions correctly! "
                              "You might want to look at the hints.")
            comment_colour = "#F8CECC"
        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        heading_font = ("Arial", 16, "bold")
        normal_font = ("Arial", 14)
        comment_font = ("Arial", 13)

        # Label List (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [rounds_string, normal_font, "W"],
            [correct_string, normal_font, "W"],
            [incorrect_string, normal_font, "W"],
            [success_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[5]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartGame()
    root.mainloop()