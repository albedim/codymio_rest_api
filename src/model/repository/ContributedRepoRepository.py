from src.configuration.config import sql
from src.model.entity.ContributedRepo import ContributedRepo


class ContributedRepoRepository:

    @classmethod
    def create(cls, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody):
        contributedRepo = ContributedRepo(issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody)
        sql.session.add(contributedRepo)
        sql.session.commit()
        return contributedRepo

    @classmethod
    def get(cls, userId):
        contributedRepos = sql.session.query(ContributedRepo).filter(ContributedRepo.user_id == userId).all()
        return contributedRepos