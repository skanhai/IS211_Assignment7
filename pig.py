import random
import argparse


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_turn_score = 0

    def roll(self):
        roll = random.randint(1, 6)
        print(f"{self.name} rolled: {roll}")
        if roll == 1:
            print(f"{self.name} rolled a 1. Turn total is reset to 0.")
            self.current_turn_score = 0
            return 1
        else:
            self.current_turn_score += roll
            print(f"{self.name}'s turn total is now: {self.current_turn_score}")
            return 0

    def hold(self):
        self.score += self.current_turn_score
        print(f"{self.name} holds. Total score is now: {self.score}")
        self.current_turn_score = 0


class Die:
    @staticmethod
    def roll():
        return random.randint(1, 6)


class Game:
    def __init__(self, num_players, game_number):
        self.num_players = num_players
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        self.current_player = 0
        self.game_number = game_number

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def reset_game_state(self):
        for player in self.players:
            player.score = 0
            player.current_turn_score = 0

    def play(self):
        self.reset_game_state()
        print(f"Starting game {self.game_number}...")
        while all(player.score < 100 for player in self.players):
            print("\n")
            print(f"Game {self.game_number}: It's {self.players[self.current_player].name}'s turn.")
            player_choice = input("Type 'r' to roll or 'h' to hold. Enter 'q' to switch to another game: ").lower()
            if player_choice == 'r':
                roll_result = self.players[self.current_player].roll()
                if roll_result == 1:
                    self.next_player()
            elif player_choice == 'h':
                self.players[self.current_player].hold()
                self.next_player()
            elif player_choice == 'q':
                return

        winner = max(self.players, key=lambda x: x.score)

        print(f"Game {self.game_number} over. {winner.name} wins with a score of {winner.score}.")

        print()


def get_valid_input(prompt, choices):
    while True:
        user_input = input(prompt).lower()
        if user_input == '':
            print("Please enter a valid input.")
            continue
        if user_input in choices:
            return user_input
        print("Invalid input. Please try again.")


def main(num_players, num_games):
    random.seed(0)
    games = []
    for game_number in range(1, num_games + 1):
        game = Game(num_players, game_number)
        games.append(game)

    current_game = None
    while True:
        if current_game is None:
            game_choice = get_valid_input("Enter the game number you want to play (0 to quit): ",
                                          ['0'] + [str(i) for i in range(1, num_games + 1)])
            game_choice = int(game_choice)
            if game_choice == 0:
                break
            current_game = games[game_choice - 1]
            current_game.play()
        else:
            game_choice = get_valid_input("Enter the game number you want to switch to (0 to quit): ",
                                          ['0'] + [str(i) for i in range(1, num_games + 1)])
            game_choice = int(game_choice)
            if game_choice == 0:
                break
            current_game = games[game_choice - 1]
            current_game.play()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", type=int, default=2)
    parser.add_argument("--numGames", type=int, default=1)
    args = parser.parse_args()

    main(args.numPlayers, args.numGames)
