from planner import Planner, UserPreferences
from local_scanner import Scanner


def main():
    user_pref = UserPreferences(2000, 100, 200, 50, ['eggs'], True, False, False, True, ['Twigs'])
    scanner = Scanner()
    scanner.scan()

    planner = Planner(scanner.calendar, user_pref)
    planner.filter()
    planner.display()


if __name__ == "__main__":
    main()