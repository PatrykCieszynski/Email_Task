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


    def getEmail(self):
        return self.local_part + "@" + self.domain + "." + self.last_part


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


def search_emails_by_text(string):
    counter = 0
    found_emails = []
    for email in Email.container:
        if string in email.local_part:
            counter += 1
            found_emails.append(email.getEmail())
    if counter > 0:
        print("Found emails with '" + string + "' in email (" + str(counter) + "):")
        for email in found_emails:
            print(email)
    else:
        print("Email not found")


if __name__ == '__main__':
    emails = Email
    files = File()
    show_incorrect_emails()
    search_emails_by_text("agustin")
