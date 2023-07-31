import requests

from src.model.entity.ContributedRepo import ContributedRepo
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils
from src.model.repository.ContributedRepoRepository import ContributedRepoRepository


class ContributedRepoService:

    @classmethod
    def create(cls, request):
        contributedRepo = ContributedRepoRepository.create(
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
    def getStatus(cls, token, e: ContributedRepo, userId):

        merged = False
        res = requests.get("https://api.github.com/repos/" + e.repo_full_name + "/pulls",
                           headers={"Authorization": "Bearer " + token})
        res = res.json()
        try:
            if not e.pushed:
                for r in res:
                    if r['user']['id'] == userId:
                        e = ContributedRepoRepository.setPushed(e)
            else:
                merged = True
                for r in res:
                    if r['user']['id'] == userId:
                        merged = False
                if merged:
                    e = ContributedRepoRepository.setMerged(e)
        except TypeError:
            pass

        return {
            'pushed': e.pushed,
            'waiting': e.pushed and not merged,
            'merged': merged
        }

    @classmethod
    def get(cls, token, userId):
        contributedRepos: list[ContributedRepo] = ContributedRepoRepository.get(userId)
        user = UserRepository.getUserById(userId)
        res = {
            "unseen": 0,
            "merged": [],
            "unmerged": []
        }
        for e in contributedRepos:
            r = cls.getStatus(token, e, user.user_github_id)
            if r['merged']:
                res['merged'].append(e.toJSON(status=r))
                if e.unseen:
                    res['unseen'] += 1
            else:
                res['unmerged'].append(e.toJSON(status=r))

        return Utils.createSuccessResponse(True, res)

    @classmethod
    def setSeen(cls, request):
        res = ContributedRepoRepository.get(request['user_id'])
        for r in res:
            if r.merged:
                ContributedRepoRepository.setSeen(r)
        return Utils.createSuccessResponse(True, Constants.CREATED)

    @classmethod
    def remove(cls, contributedRepoId):
        res = ContributedRepoRepository.remove(contributedRepoId)
        return Utils.createSuccessResponse(True, Constants.CREATED)

