import sys

from cashflower import start
from tutorials.life_insurance.endowment.settings import settings


if __name__ == "__main__":
    start("tutorials.life_insurance.endowment", settings, sys.argv)