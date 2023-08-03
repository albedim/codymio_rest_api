from sqlalchemy import desc

from src.configuration.config import sql
from src.model.entity.Contribution import Contribution


class ContributionRepository:

    @classmethod
    def create(cls, issueNumber, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody):
        contributedRepo = Contribution(issueNumber, issueOwner, userId, repoId, repoFullName, issueId, issueTitle, issueBody)
        sql.session.add(contributedRepo)
        sql.session.commit()
        return contributedRepo

    @classmethod
    def get(cls, userId):
        contributedRepos = sql.session.query(Contribution)\
            .filter(Contribution.user_id == userId).order_by(desc(Contribution.contribution_id)).all()
        return contributedRepos

    @classmethod
    def remove(cls, contributionId):
        contributedRepo = sql.session.query(Contribution).filter(Contribution.contribution_id == contributionId).delete()
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

    @classmethod
    def getByRepoIdAndUserId(cls, repoId, userId):
        contribution = sql.session.query(Contribution).filter(Contribution.repo_id == repoId)\
            .filter(Contribution.user_id == userId).first()
        return contribution