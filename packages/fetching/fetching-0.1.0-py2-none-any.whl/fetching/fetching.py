import github
import os


class Handler:
    def __init__(self, name: str, auth: str):
        self.repo = github.Github(auth).get_repo(name)

    def get_file(self, file_path: str, ref: [str, None]):

        content = \
            self.repo.get_contents(file_path, ref=ref) \
            if ref is not None \
            else self.repo.get_contents(file_path)

        return content.decoded_content.decode("utf-8")

    def get_files(self, files: list, commit: [str, None]):
        return [self.get_file(file, commit) for file in files]


class Fetching:

    @staticmethod
    def resolve_token(token: [str, None]):
        """
        resolve API token according to order of precedence from
        GH docs: https://cli.github.com/manual/gh_help_environment
        """

        if token is not None:
            return token
        elif os.getenv("GH_TOKEN") is not None:
            return os.getenv("GH_TOKEN")
        elif os.getenv("GITHUB_TOKEN") is not None:
            return os.getenv("GITHUB_TOKEN")
        else:
            raise ValueError("Unable to locate GitHub API token.")

    def fetch(self, targets: list, token: [str, None] = None):

        ret = []
        token = self.resolve_token(token)
        for t in targets:
            ret.append(
                Handler(t.get("name"), token).get_files(t.get("files"), t.get("ref"))
            )

        return ret

    @staticmethod
    def _filter_main(f: str):
        """
        extract contents of file up until main invocation, if it exists
        """

        lines = f.split("\n")
        ret = []
        for l in lines:
            if ("if __name__ == '__main__'" in l) or ("if __name__ == \"__main__\"" in l):
                break
            else:
                ret.append(l)

        return "\n".join(ret)

    def build(self, dependencies: list):
        return "\n".join("\n".join([self._filter_main(f) for f in d]) for d in dependencies)

    @staticmethod
    def write(dest: str, content: str):
        with open(dest, "w") as out:
            out.write(content)

    def fetch_and_build(self, targets: list, token: [str, None]):

        dependencies = self.fetch(targets, token)
        content = self.build(dependencies)

        return content
