from os import listdir
import re
import csv


class Email:
    container = []
    bad_emails = []

    def __init__(self, local_part, domain, last_part):
        self.local_part = local_part
        self.domain = domain
        self.last_part = last_part

    @staticmethod
    def match_email(email):
        PATTERN = re.compile("(.+)@(.+)\.([a-zA-Z0-9]{1,4})")
        if PATTERN.match(email):
            Email.container.append(
                Email(PATTERN.match(email).group(1), PATTERN.match(email).group(2), PATTERN.match(email).group(3)))
        else:
            Email.bad_emails.append(email.split("\n")[0])


class File:
    PATH = "./Resources/emails/"
    container = []

    def __init__(self):
        for filename in listdir(self.PATH):
            file = open(self.PATH + filename, 'r')
            self.parse_file(file, filename.split('.')[1])
            file.close()

    @staticmethod
    def parse_file(file, extension):
        if extension == "txt":
            lines = file.readlines()
            for line in lines:
                Email.match_email(line)
        else:
            csvfile = csv.DictReader(file, delimiter=";")
            for row in csvfile:
                Email.match_email(row["email"])


def show_incorrect_emails():
    print("Invalid emails (" + str(len(Email.bad_emails)) + "):")
    for email in Email.bad_emails:
        print("\t" + email)


if __name__ == '__main__':
    emails = Email
    files = File()
    show_incorrect_emails()
