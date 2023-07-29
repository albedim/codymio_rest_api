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

        if not e.pushed:
            res = requests.get("https://api.github.com/repos/" + e.repo_full_name + "/pulls",
                               headers={"Authorization": "Bearer "+token})
            res = res.json()
            for r in res:
                if r['user']['id'] == userId:
                    ContributedRepoRepository.setPushed(e)
        res = requests.get("https://api.github.com/repos/"+e.repo_full_name+"/pulls/"+str(e.issue_number),
                           headers={"Authorization": "Bearer "+token})
        res = res.json()
        print(res)
        r = {
            'pushed': e.pushed,
            'waiting': e.pushed and res['merged_at'] is None,
            'merged': res['merged_at'] is not None
        }
        return r

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
                    ContributedRepoRepository.setSeen(e)
            else:
                res['unmerged'].append(e.toJSON(status=r))

        return Utils.createSuccessResponse(True, res)