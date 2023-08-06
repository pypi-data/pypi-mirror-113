import os

from snake.md import Document, InlineText

from generate_docs.repo import Repo, LanguageCollection


class Wiki:
    """
    An object representing a GitHub wiki.
    """

    def __init__(self, repo: Repo):
        """
        Constructs an instance of a Wiki.
        :param repo: a GitHub repository object
        """
        self.repo: Repo = repo
        self.wiki_url_base: str = "/TheRenegadeCoder/sample-programs/wiki/"
        self.repo_url_base: str = "/TheRenegadeCoder/sample-programs/tree/main/archive/"
        self.issue_url_base: str = "/TheRenegadeCoder/sample-programs/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        self.pages: list[Document] = list()
        self._build_alphabet_catalog()
        self._build_alphabet_pages()

    def _build_wiki_link(self, text: str, page_name: str) -> str:
        """
        A helper method which creates a link to a wiki page.
        (e.g., https://github.com/TheRenegadeCoder/sample-programs/wiki/S)
        :param text: the text to display for the link
        :param page_name: the name of the page to link
        :return: a markdown link to a wiki page
        """
        return str(InlineText(text, url=f"{self.wiki_url_base}{page_name}"))

    def _build_repo_link(self, text: str, letter: str, language: str) -> str:
        """
        A helper method which creates a link to the language folder in the repo
        (e.g., https://github.com/TheRenegadeCoder/sample-programs/tree/main/archive/c/c-sharp.)
        :param text: the link text
        :param letter: the starting letter of the language
        :param language: the language to link
        :return: a markdown link to a sample programs language page
        """
        return str(InlineText(text, url=f"{self.repo_url_base}{letter}/{language}"))

    def _build_issue_link(self, language: str) -> str:
        """
        A helper method which creates a link to all issues matching that language.
        :param language: the language to search for issues
        :return: a markdown link to a GitHub query for issues matching this language
        """
        lang_query = language.replace("-", "+")
        return str(InlineText("Here", f"{self.issue_url_base}{lang_query}"))

    def _build_test_link(self, language: LanguageCollection, letter: str) -> str:
        """
        A helper method which creates a link to the test file for a given language collection.
        :param language: a language collection
        :param letter: the first letter of the language
        :return: a markdown link to a test file if it exists; an empty string otherwise
        """
        test_file_path = language.test_file_path
        if test_file_path:
            file_path = self.repo_url_base + letter + "/" + language.name + "/" + os.path.basename(test_file_path)
            file_path_link = str(InlineText("Here", url=file_path))
        else:
            file_path_link = ""
        return file_path_link

    @staticmethod
    def _build_language_link(language: LanguageCollection) -> str:
        """
        A handy abstraction for the create_md_link() method which creates a link to a sample programs language page.
        (e.g., https://sample-programs.therenegadecoder.com/languages/c/)
        :param language: the language to link
        :return: a markdown link to the language page if it exists; an empty string otherwise
        """
        lang = InlineText("Here", language.sample_program_url)
        if not lang.verify_url():
            lang = InlineText("")
        return str(lang)

    def _build_alphabet_page(self, letter: str):
        """
        A helper method which generates a single wiki alphabet page given a letter.
        :param letter: the starting letter of a set of programming languages (e.g., "p" for [pascal, perl, python])
        :return:
        """
        page = Document(letter.capitalize())
        page.add_paragraph(
            f"""
            The following table contains all the existing languages in the repository that start with the letter 
            {letter.capitalize()}:
            """
        )
        header = ["Language", "Article(s)", "Issue(s)", "Test(s)", "# of Snippets"]
        body = []
        languages_by_letter = self.repo.get_languages_by_letter(letter)
        total_snippets = 0
        for language in languages_by_letter:
            total_snippets += language.total_snippets
            language_link = self._build_repo_link(language.name.capitalize(), letter, language.name)
            tag_link = self._build_language_link(language)
            issues_link = self._build_issue_link(language.name)
            tests_link = self._build_test_link(language, letter)
            body.append([language_link, tag_link, issues_link, tests_link, str(language.total_snippets)])
        body.append(["**Totals**", "", "", "", str(total_snippets)])
        page.add_table(header, body)
        return page

    def _build_alphabet_pages(self) -> None:
        """
        Builds a set of wiki alphabet pages from the repo.
        :return: None
        """
        alphabetical_list = self.repo.get_sorted_language_letters()
        for index, letter in enumerate(alphabetical_list):
            page = self._build_alphabet_page(letter)
            previous_index = index - 1
            next_index = (index + 1) % len(alphabetical_list)
            previous_letter = alphabetical_list[previous_index].capitalize()
            next_letter = alphabetical_list[next_index].capitalize()
            previous_text = f"Previous ({previous_letter})"
            next_text = f"Next ({next_letter})"
            previous_link = self._build_wiki_link(previous_text, previous_letter)
            next_link = self._build_wiki_link(next_text, next_letter)
            page.add_paragraph(" ".join(["<", previous_link, "|", next_link, ">"]))
            self.pages.append(page)

    def _build_alphabet_catalog(self) -> None:
        """
        Builds a wiki alphabet catalog from the repo.
        :return: None
        """
        page = Document("Alphabetical Language Catalog")
        alphabetical_list = self.repo.get_sorted_language_letters()
        header = ["Collection", "# of Languages", "# of Snippets", "# of Tests"]
        body = []
        for letter in alphabetical_list:
            letter_link = self._build_wiki_link(letter.capitalize(), letter.capitalize())
            languages_by_letter = self.repo.get_languages_by_letter(letter)
            num_of_languages = len(languages_by_letter)
            num_of_snippets = sum([language.total_snippets for language in languages_by_letter])
            num_of_tests = sum([1 if language.test_file_path else 0 for language in languages_by_letter])
            body.append([letter_link, str(num_of_languages), str(num_of_snippets), str(num_of_tests)])
        body.append([
            "**Totals**",
            str(len(self.repo.languages)),
            str(self.repo.total_snippets),
            str(self.repo.total_tests)
        ])
        page.add_table(header, body)
        self.pages.append(page)
