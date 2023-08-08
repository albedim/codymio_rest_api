import requests

from src.model.entity.Contribution import Contribution
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils
from src.model.repository.ContributionRepository import ContributionRepository


class ContributionService:

    @classmethod
    def create(cls, request):
        if cls.hasContributed(request['issue_id'], request['repo_id'], request['user_id']):
            return Utils.createWrongResponse(False, Constants.ALREADY_CREATED, 409), 409
        contributedRepo = ContributionRepository.create(
            request['issue_number'],
            request['issue_owner'],
            request['user_id'],
            request['repo_id'],
            request['repo_full_name'],
            request['issue_id'],
            request['issue_title'],
            request['issue_body']
        )
        return Utils.createSuccessResponse(True, Constants.CREATED)

    @classmethod
    def updateStatus(cls, token, userId, e: Contribution):

        res = requests.get("https://api.github.com/repos/" + e.repo_full_name + "/pulls",
                           headers={"Authorization": "Bearer " + token}).json()
        try:
            if not e.pushed:
                for r in res:
                    if r['user']['id'] == userId:
                        e = ContributionRepository.setPushed(e)
            else:
                merged = True
                for r in res:
                    if r['user']['id'] == userId:
                        merged = False
                if merged:
                    e = ContributionRepository.setMerged(e)
        except TypeError:
            pass

        if not e.pushed:
            return 'none'
        if e.pushed and not e.merged:
            return 'pushed'
        if e.merged:
            return 'completed'

    @classmethod
    def get(cls, token, userId):
        contributedRepos: list[Contribution] = ContributionRepository.get(userId)
        user = UserRepository.getUserById(userId)
        res = {
            "unseen": 0,
            "completed": [],
            "uncompleted": []
        }
        for e in contributedRepos:
            if e.merged:
                res['completed'].append(e.toJSON(
                    status="completed",
                    removable=False
                ))
                if e.unseen:
                    res['unseen'] += 1
            else:
                r = cls.updateStatus(token, user.user_github_id, e)
                res['uncompleted'].append(e.toJSON(removable=True, status=r))

        return Utils.createSuccessResponse(True, res)

    @classmethod
    def setSeen(cls, request):
        res = ContributionRepository.get(request['user_id'])
        for r in res:
            if r.merged:
                ContributionRepository.setSeen(r)
        return Utils.createSuccessResponse(True, Constants.CREATED)

    @classmethod
    def remove(cls, contributedRepoId):
        res = ContributionRepository.remove(contributedRepoId)
        return Utils.createSuccessResponse(True, Constants.CREATED)

    @classmethod
    def hasContributed(cls, issueId, repoId, userId):
        contribution = ContributionRepository.getByRepoIdAndUserId(
            issueId,
            repoId,
            userId
        )
        return contribution is not None

    @classmethod
    def contributable(cls, repoId, userId):
        contribution = ContributionRepository.getUnmergedContributions(
            repoId,
            userId
        )
        return contribution is None

