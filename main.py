from os import listdir
import re
import csv
from itertools import groupby

PATTERN = re.compile("(.+)@(.+)\.([a-zA-Z0-9]{1,4})")
PATH = "./Resources/emails/"


class EmailContainer:
    def __init__(self, path=None):
        self.container = set()
        self.bad_emails = []
        self.emails_sent = set()
        if path is not None:
            self.parse_files(path)

    def parse_files(self, path):
        files = []
        try:
            files = listdir(path)
        except FileNotFoundError:
            print("Emails directory not found")
            quit()
        for filename in files:
            extension = (filename.split('.')[1]).lower()
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

    def show_incorrect_emails(self):
        print("Invalid emails (" + str(len(self.bad_emails)) + "):")
        for email in self.bad_emails:
            print("\t" + str(email))

    def search_emails_by_text(self, string):
        counter = 0
        found_emails = []
        for email in self.container:
            if string in email.unique_name:
                counter += 1
                found_emails.append(email)
        if counter > 0:
            print("Found emails with '" + string + "' in email (" + str(counter) + "):")
            for email in found_emails:
                print("\t" + str(email))
        else:
            print("Email not found")

    def group_by_domain(self):
        sorted_emails = sorted(self.container, key=lambda x: (x.domain, x.unique_name))
        grouped_emails = [list(domains) for key, domains in groupby(sorted_emails, key=lambda x: x.domain)]
        for domain in grouped_emails:
            print("Domain " + domain[0].domain + " (" + str(domain.__len__()) + "):")
            for email in domain:
                print("\t" + str(email))

    def parse_log_file(self, path_to_log_file):
        file = None
        try:
            extension = (path_to_log_file.split('.')[-1]).lower()
            if extension == "logs":
                file = open(path_to_log_file, 'r')
                lines = file.readlines()
                for line in lines:
                    self.emails_sent.add(Email.match_email(re.search("\'(.+)\'", line).group(1)))
            else:
                raise ValueError
        except AttributeError:
            print("Log file has wrong format")
            quit()
        except FileNotFoundError:
            print("Log file not found")
            quit()
        except PermissionError:
            print("No permission to access file")
            quit()
        except ValueError:
            print("Log file has wrong extension")
            quit()
        finally:
            if file is not None:
                file.close()

    def find_emails_not_in_logs(self, path_to_log_file):
        self.parse_log_file(path_to_log_file)
        unused_emails = list(self.container.difference(self.emails_sent))
        unused_emails = sorted(unused_emails, key=lambda x: x.unique_name)
        print("Emails not sent (" + str(unused_emails.__len__()) + "):")
        for mail in unused_emails:
            print("\t" + str(mail))


class UniqueName:
    def __init__(self, unique_name):
        self.unique_name = unique_name


class Domain:
    def __init__(self, domain):
        domain = domain.split(".")
        self.domain = domain[0]
        self.domain_type = domain[1]

    def __str__(self):
        return self.domain + "." + self.domain_type


class Email(UniqueName, Domain):
    def __init__(self, unique_name, domain):
        UniqueName.__init__(self, unique_name)
        Domain.__init__(self, domain)

    @staticmethod
    def match_email(email):
        if email is not None:
            if PATTERN.match(email):
                return Email(PATTERN.match(email).group(1),
                             PATTERN.match(email).group(2) + "." + PATTERN.match(email).group(3))
            else:
                return email.split("\n")[0]

    def __str__(self):
        return self.unique_name + "@" + self.domain + "." + self.domain_type

    def __eq__(self, other):
        return self.unique_name == other.unique_name and \
               self.domain == other.domain and \
               self.domain_type == other.domain_type

    def __hash__(self):
        return hash(("unique_name", self.unique_name,
                    "domain", self.domain + "." + self.domain_type))


def choose_menu():
    while True:
        print("1. Show incorrect emails")
        print("2. Search emails by text")
        print("3. Group emails by domain")
        print("4. Find emails that are not in the logs file")
        print("Any other input will quit")
        choice = input("Choose option number: ")
        if choice == "1":
            emails.show_incorrect_emails()
        elif choice == "2":
            text = input("For what text should I search?: ")
            emails.search_emails_by_text(text)
        elif choice == "3":
            emails.group_by_domain()
        elif choice == "4":
            emails.find_emails_not_in_logs("./Resources/email-sent.logs")
        else:
            print("Exiting...")
            quit()


if __name__ == '__main__':
    emails = EmailContainer(PATH)
    choose_menu()
