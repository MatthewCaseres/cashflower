import sys

from cashflower import start
from tutorials.life_insurance.term_life.settings import settings


if __name__ == "__main__":
    start("tutorials.life_insurance.term_life", settings, sys.argv)