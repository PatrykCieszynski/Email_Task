from os import listdir
import re
import csv
from itertools import groupby

PATTERN = re.compile('(.+)@(.+)\.([a-zA-Z0-9]{1,4})')
PATH = "./Resources/emails/"


class Email:
    container = set()
    bad_emails = []

    def __init__(self, local_part, domain):
        self.local_part = local_part
        self.domain = domain

    @staticmethod
    def match_email(email):
        if PATTERN.match(email):
            Email.container.add(
                Email(PATTERN.match(email).group(1),
                      PATTERN.match(email).group(2) + "." + PATTERN.match(email).group(3)))
        else:
            Email.bad_emails.append(email.split("\n")[0])

    def __str__(self):
        return self.local_part + "@" + self.domain

    def __eq__(self, other):
        return self.local_part == other.local_part and self.domain == other.domain

    def __hash__(self):
        return hash(("local_part", self.local_part,
                    "domain", self.domain))


class File:
    def __init__(self):
        for filename in listdir(PATH):
            file = open(PATH + filename, 'r')
            self.parse_file(file, filename.split('.')[1])
            file.close()

    @staticmethod
    def parse_file(file, extension):
        if extension == "txt":
            lines = file.readlines()
            for line in lines:
                Email.match_email(line)
        elif extension == "csv":
            csvfile = csv.DictReader(file, delimiter=";")
            for row in csvfile:
                Email.match_email(row["email"])


def show_incorrect_emails():
    print("Invalid emails (" + str(len(Email.bad_emails)) + "):")
    for email in Email.bad_emails:
        print("\t" + email)


def search_emails_by_text(string):
    counter = 0
    found_emails = []
    for email in Email.container:
        if string in email.local_part:
            counter += 1
            found_emails.append(email)
    if counter > 0:
        print("Found emails with '" + string + "' in email (" + str(counter) + "):")
        for email in found_emails:
            print(email)
    else:
        print("Email not found")


def group_by_domain():
    sorted_emails = sorted(Email.container, key=lambda x: (x.domain, x.local_part))
    grouped_emails = [list(domains) for key, domains in groupby(sorted_emails, key=lambda x: x.domain)]
    for domain in grouped_emails:
        print("Domain " + domain[0].domain + " (" + str(domain.__len__()) + "):")
        for email in domain:
            print("\t" + str(email))


if __name__ == '__main__':
    emails = Email
    files = File()
    # show_incorrect_emails()
    # search_emails_by_text("agustin")
    # group_by_domain()
