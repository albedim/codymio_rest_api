from sqlalchemy import desc

from src.configuration.config import sql
from src.model.entity.ContributedRepo import ContributedRepo


class ContributedRepoRepository:

    @classmethod
    def create(cls, issueNumber, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody):
        contributedRepo = ContributedRepo(issueNumber, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody)
        sql.session.add(contributedRepo)
        sql.session.commit()
        return contributedRepo

    @classmethod
    def get(cls, userId):
        contributedRepos = sql.session.query(ContributedRepo).filter(ContributedRepo.user_id == userId).order_by(desc(ContributedRepo.contributed_id)).all()
        return contributedRepos

    @classmethod
    def remove(cls, contributedRepoId):
        contributedRepo = sql.session.query(ContributedRepo).filter(ContributedRepo.contributed_id == contributedRepoId).delete()
        sql.session.commit()
        return contributedRepo

    @classmethod
    def setPushed(cls, e):
        e.pushed = True
        sql.session.commit()
        return e

    @classmethod
    def setSeen(cls, e):
        e.unseen = False
        sql.session.commit()
        return e

    @classmethod
    def setMerged(cls, e):
        e.merged = True
        sql.session.commit()
        return e