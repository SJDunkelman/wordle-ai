import argparse
from game import Wordle
from naive import naive_bot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play or simulate Wordle')
    parser.add_argument('-n', action='store', default=1, dest='rounds', type=int, nargs=1,
                        help='how many rounds to play or simulate')
    parser.add_argument('-m', dest='manual', help='run manually', action='store_true')
    parser.add_argument('-b', dest='bot', help='run a naive bot', action='store_true')
    parser.add_argument('-v', dest='verbose', default=False, help='print verbose', action='store_true')
    args = parser.parse_args()

    assert args.bot or args.manual, 'Must select whether bot simulating play (-b) or user playing manually (-m)'

    if args.manual:
        g = Wordle(manual=args.manual,
                   verbose=args.verbose,
                   rounds=args.rounds)
    else:
        g = Wordle(manual=args.manual,
                   verbose=args.verbose,
                   rounds=args.rounds,
                   bot=naive_bot)
