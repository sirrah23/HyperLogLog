"""
Generates data that can be used to test the HyperLogLog algorithm
implementation.
"""
import random
from datetime import datetime

def new_filename():
    """
    Generates a filename that data can be written to using the current
    date-time.
    """
    now = datetime.now()
    date = str(now.date()).replace("-", "")
    time = str(now.time()).replace(".", "").replace(":", "")
    return "data_{}{}.csv".format(date, time)


def generate_data_even(dates, products, rows=10000):
    """
    Generate data so that date/product pairs are evenly distributed.
    """
    for i in range(rows):
        yield (random.choice(dates), random.choice(products))

def generate_data_weighted(dates, products, rows=10000):
    """
    Generates data so that the number of distinct items for each date will vary
    wildly.
    """
    rem_rows = rows
    while rem_rows > 0:
        rows_write = random.randint(1, rem_rows)
        rem_rows -= rows_write
        curr_date = random.choice(dates)
        while rows_write > 0:
            curr_prod = random.choice(products)
            yield (curr_date, curr_prod)
            rows_write -= 1

def write_data(dates, products, out_file):
    """
    Generates data which is then written to the specified file in csv format.
    """
    gen = generate_data_weighted(dates, products)
    with open(out_file, "a") as f:
        f.write("date,product\n")
        for i in gen:
            f.write("{},{}\n".format(i[0], i[1]))

def read_values(in_file):
    """
    Reads newline delimited values and returns them in a list.
    """
    with open(in_file, "r") as f:
        data = f.read().splitlines()
    return data

if __name__ == "__main__":
    dates = read_values("./in/dates.txt")  # Read list of possible dates
    products = read_values("./in/products.txt")  # Read list of possible products
    out_file = "./data/{}".format(new_filename())  # File to write data to
    write_data(dates, products, out_file)  # Generate the data!

