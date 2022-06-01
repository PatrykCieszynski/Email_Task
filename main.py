from os import listdir
import re
import csv
from itertools import groupby

PATTERN = re.compile("(.+)@(.+)\.([a-zA-Z0-9]{1,4})")
PATH = "./Resources/emails/"


class EmailContainer:

    def __init__(self):
        self.container = set()
        self.bad_emails = []

    def parse_files(self, path):
        for filename in listdir(path):
            extension = filename.split('.')[1]
            file = open(path + filename, 'r')
            if extension == "txt":
                lines = file.readlines()
                for line in lines:
                    result = Email.match_email(line)
                    if type(result) is Email:
                        self.container.add(result)
                    else:
                        self.bad_emails.append(result)
            elif extension == "csv":
                csvfile = csv.DictReader(file, delimiter=";")
                for row in csvfile:
                    result = Email.match_email(row["email"])
                    if type(result) is Email:
                        self.container.add(result)
                    else:
                        self.bad_emails.append(result)
            file.close()
        return emails

    def show_incorrect_emails(self):
        print("Invalid emails (" + str(len(self.bad_emails)) + "):")
        for email in self.bad_emails:
            print("\t" + str(email))

    def group_by_domain(self):
        sorted_emails = sorted(self.container, key=lambda x: (x.domain, x.local_part))
        grouped_emails = [list(domains) for key, domains in groupby(sorted_emails, key=lambda x: x.domain)]
        for domain in grouped_emails:
            print("Domain " + domain[0].domain + " (" + str(domain.__len__()) + "):")
            for email in domain:
                print("\t" + str(email))

    def search_emails_by_text(self, string):
        counter = 0
        found_emails = []
        for email in self.container:
            if string in email.local_part:
                counter += 1
                found_emails.append(email)
        if counter > 0:
            print("Found emails with '" + string + "' in email (" + str(counter) + "):")
            for email in found_emails:
                print(email)
        else:
            print("Email not found")


class Email:
    bad_emails = []

    def __init__(self, local_part, domain):
        self.local_part = local_part
        self.domain = domain

    @staticmethod
    def match_email(email):
        if PATTERN.match(email):
            return Email(PATTERN.match(email).group(1),
                         PATTERN.match(email).group(2) + "." + PATTERN.match(email).group(3))
        else:
            return email.split("\n")[0]

    def __str__(self):
        return self.local_part + "@" + self.domain

    def __eq__(self, other):
        return self.local_part == other.local_part and self.domain == other.domain

    def __hash__(self):
        return hash(("local_part", self.local_part,
                    "domain", self.domain))


if __name__ == '__main__':
    emails = EmailContainer()
    emails.parse_files(PATH)
    # emails.show_incorrect_emails()
    # emails.search_emails_by_text("agustin")
    # emails.group_by_domain()
