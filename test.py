from unittest import TestCase, main as run_tests

import main


class TestEmailMatching(TestCase):
    def test_none(self):
        data = None
        result = main.Email.match_email(data)
        self.assertIsNone(result)

    def test_invalid(self):
        data = "patrykciesz@gmail"
        result = main.Email.match_email(data)
        self.assertIsInstance(result, str)
        self.assertEqual(result, data)

    def test_valid(self):
        data = "patrykciesz@gmail.com"
        result = main.Email.match_email(data)
        self.assertIsInstance(result, main.Email)
        self.assertEqual(result.local_part, "patrykciesz")
        self.assertEqual(result.domain, "gmail.com")


class TestEmailContainer(TestCase):
    def test_empty_directory(self):
        result = main.EmailContainer("./Tests_Resources/Empty_directory/")
        self.assertIsInstance(result, main.EmailContainer)
        self.assertFalse(result.container)
        self.assertFalse(result.bad_emails)
        self.assertFalse(result.emails_sent)

    def test_nonexisting_directory(self):
        container = main.EmailContainer()
        self.assertRaises(SystemExit, container.parse_files, "./Tests_Resources/Cool_directory/")

    def test_wrong_extension(self):
        result = main.EmailContainer("./Tests_Resources/Emails_wrong_extension/")
        self.assertIsInstance(result, main.EmailContainer)
        self.assertFalse(result.container)
        self.assertFalse(result.bad_emails)
        self.assertFalse(result.emails_sent)

    def test_empty_files(self):
        result = main.EmailContainer("./Tests_Resources/Emails_empty_files/")
        self.assertIsInstance(result, main.EmailContainer)
        self.assertFalse(result.container)
        self.assertFalse(result.bad_emails)
        self.assertFalse(result.emails_sent)

    def test_valid(self):
        result = main.EmailContainer("./Tests_Resources/Emails_valid/")
        self.assertIsInstance(result, main.EmailContainer)
        self.assertTrue(result.container)
        self.assertTrue(result.bad_emails)
        self.assertFalse(result.emails_sent)


class TestLogFiles(TestCase):
    def setUp(self):
        self.container = main.EmailContainer()

    def test_empty(self):
        path = "./Tests_Resources/Log/empty_log.logs"
        self.container.parse_log_file(path)
        self.assertFalse(self.container.emails_sent)

    def test_invalid(self):
        path = "./Tests_Resources/Log/invalid_log.logs"
        self.assertRaises(SystemExit, self.container.parse_log_file, path)

    def test_wrong_format(self):
        path = "./Tests_Resources/Log/valid_log.txt"
        self.assertRaises(SystemExit, self.container.parse_log_file, path)

    def test_nonexisting(self):
        path = "./Tests_Resources/Log/cool_log.logs"
        self.assertRaises(SystemExit, self.container.parse_log_file, path)

    def test_valid(self):
        path = "./Tests_Resources/Log/valid_log.logs"
        self.container.parse_log_file(path)
        result = None
        for first_item in self.container.emails_sent:
            result = first_item
            break
        self.assertTrue(self.container.emails_sent)
        self.assertIsInstance(result, main.Email)


if __name__ == "__main__":
    run_tests()
