from src.utils.Constants import Constants
from src.utils.Utils import Utils
from src.model.repository.ContributedRepoRepository import ContributedRepoRepository


class ContributedRepoService:

    @classmethod
    def create(cls, request):
        print(request)
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
    def get(cls, userId):
        contributedRepos = ContributedRepoRepository.get(userId)
        res = []
        for e in contributedRepos:
            res.append(e.toJSON())
        return Utils.createSuccessResponse(True, Utils.createListOfPages(res, 4))