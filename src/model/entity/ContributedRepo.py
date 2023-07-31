import datetime
from src.configuration.config import sql


class ContributedRepo(sql.Model):
    __tablename__ = 'contributed_repos'
    contributed_id: int = sql.Column(sql.Integer, primary_key=True)
    unseen: bool = sql.Column(sql.Boolean, nullable=False)
    merged: bool = sql.Column(sql.Boolean, nullable=False)
    pushed: bool = sql.Column(sql.Boolean, nullable=False)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    repo_id: int = sql.Column(sql.Integer, nullable=False)
    repo_full_name: str = sql.Column(sql.String(140), nullable=False)
    issue_id: int = sql.Column(sql.Integer, nullable=False)
    issue_number: int = sql.Column(sql.Integer, nullable=False)
    issue_owner: str = sql.Column(sql.String(40), nullable=False)
    issue_title: str = sql.Column(sql.String(140), nullable=False)
    issue_body: str = sql.Column(sql.String(840), nullable=False)

    def __init__(self, issueNumber, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody):
        self.user_id = userId
        self.issue_number = issueNumber
        self.repo_id = repoId
        self.repo_full_name = repoFullName
        self.issue_id = issueId
        self.issue_owner = issueOwner
        self.issue_title = issueTitle
        self.pushed = False
        self.unseen = True
        self.merged = False
        self.issue_body = issueBody

    def toJSON(self, **kvargs):
        obj = {
            'contributed_id': self.contributed_id,
            'user_id': self.user_id,
            'pushed': self.pushed,
            'unseen': self.unseen,
            'merged': self.merged,
            'repository': {
                'repo_id': self.repo_id,
                'repo_full_name': self.repo_full_name,
            },
            'issue': {
                'issue_id': self.issue_id,
                'issue_number': self.issue_number,
                'issue_owner': self.issue_owner,
                'issue_title': self.issue_title,
                'issue_body': self.issue_body
            }
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj