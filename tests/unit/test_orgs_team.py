import pytest

from github3 import GitHubError
from github3.orgs import Team

from .helper import UnitHelper, UnitIteratorHelper


def url_for(path=''):
    """Simple function to generate URLs with the base Org URL."""
    if path:
        path = '/' + path.strip('/')
    return 'https://api.github.com/teams/10' + path


class TestTeam(UnitHelper):
    described_class = Team
    example_data = {
        'url': 'https://api.github.com/teams/10',
        'name': 'Owners',
        'id': 10,
        'permission': 'admin',
        'members_count': 3,
        'repos_count': 10,
        'organization': {
            'login': 'github',
            'id': 1,
            'url': 'https://api.github.com/orgs/github',
            'avatar_url': 'https://github.com/images/error/octocat_happy.gif'
        }
    }

    def test_add_repository(self):
        """Show that one can add a repository to an organization team."""
        self.instance.add_repository('name-of-repo')

        self.session.put.assert_called_once_with(url_for('repos/name-of-repo'))

    def test_add_repository_requires_auth(self):
        """Show that adding a repo to a team requires authentication."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.add_repository('repo')

    def test_remove_repository(self):
        """Show that a user can remove a repository from a team."""
        self.instance.remove_repository('repo')

        self.session.delete.assert_called_once_with(url_for('/repos/repo'))

    def test_remove_repository_requires_auth(self):
        """Show that removing a repo from a team requires authentication."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.remove_repository('repo')


class TestTeamIterator(UnitIteratorHelper):
    described_class = Team

    example_data = {
        'url': url_for()
    }

    def test_members(self):
        """Show that one can iterate over all members of a Team."""
        i = self.instance.members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )

    def test_repositories(self):
        """Show that one can iterate over an organization's repositories."""
        i = self.instance.repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repos'),
            params={'per_page': 100},
            headers={}
        )