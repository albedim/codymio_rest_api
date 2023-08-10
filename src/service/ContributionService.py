import requests

from src.model.entity.Contribution import Contribution
from src.model.repository.UserRepository import UserRepository
from src.service.NotificationService import NotificationService
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
        notifications = NotificationService.create(
            Constants.ADD_CONTRIBUTION_NOTIFICATION["content"].replace("{repository}", request['repo_full_name']),
            Constants.ADD_CONTRIBUTION_NOTIFICATION['title'],
            request['user_id']
        )
        return Utils.createSuccessResponse(True, notifications)

    @classmethod
    def __updateStatus(cls, token, userId, userGithubId, e: Contribution):

        res = requests.get("https://api.github.com/repos/" + e.repo_full_name + "/pulls",
                           headers={"Authorization": "Bearer " + token}).json()
        try:
            if not e.pushed:
                for r in res:
                    if r['user']['id'] == userGithubId:
                        e = ContributionRepository.setPushed(e)
                        NotificationService.create(
                            Constants.PUSHED_NOTIFICATION['content'].replace("{repository}", e.repo_full_name),
                            Constants.PUSHED_NOTIFICATION['title'],
                            userId
                        )
                        break
            else:
                if not e.merged:
                    merged = True
                    for r in res:
                        if r['user']['id'] == userGithubId:
                            merged = False
                    if merged:
                        e = ContributionRepository.setMerged(e)
                        NotificationService.create(
                            Constants.COMPLETED_CONTRIBUTION_NOTIFICATION['content'],
                            Constants.COMPLETED_CONTRIBUTION_NOTIFICATION['title'],
                            userId
                        )
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
                r = cls.__updateStatus(token, userId, user.user_github_id, e)
                res['uncompleted'].append(e.toJSON(removable=True, status=r))

        return Utils.createSuccessResponse(True, res)

    @classmethod
    def updateStatuses(cls, token, request):
        contributedRepos: list[Contribution] = ContributionRepository.get(request['user_id'])
        user = UserRepository.getUserById(request['user_id'])
        for e in contributedRepos:
            cls.__updateStatus(token, user.user_id, user.user_github_id, e)
        return Utils.createSuccessResponse(True, Constants.CREATED)

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

