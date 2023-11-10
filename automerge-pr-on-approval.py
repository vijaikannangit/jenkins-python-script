#Auto Merge PR
import requests

def is_pr_eligible(owner, repo, pr_number, github_token):
    """
    To check the status of PR whether it is eligible for Merging
    Keyword arguments:
    -----------------
    owner : string
    repo  : string
    pr_number : number
    github_token : string
    Returns:
    --------
    PR state : string format.
        Returns PR status like clean, merged, closed, etc., 
    """    
    # Construct the API URL for the PR
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'

    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the API request to get information about the PR
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Check the 'state' field in the response JSON
        return response.json()['state']
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to fetch PR information. Status code: {response.status_code}')
        return False

# to check minimum number of PR approval is 2 and PR is approved or not 
def is_pr_approved_min_approvals(owner, repo, pr_number, github_token, minimum_approvals):
    """
    To check the status of PR whether it is approved and eligible for Merging
    Keyword arguments:
    -----------------
    owner : string
    repo  : string
    pr_number : number
    github_token : string
    minimum_approvals : number
    Returns:
    --------
    approved_count : number
        Returns count of approvers  
    """    

    # Construct the API URL for the PR

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
    
    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }


    # Make the API request to get the PR reviews
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Check if there are enough approvals
        reviews = response.json()
        approved_count = sum(1 for review in reviews if review['state'] == 'APPROVED')

        if approved_count >= minimum_approvals:
          return approved_count
        elif approved_count == 0:
          return 0
        else:
          return -1
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to fetch PR reviews. Status code: {response.status_code}')
        return -1

def automerge_pr(owner, repo, pr_number, github_token):
    """
    Automerges the PR
    Keyword arguments:
    -----------------
    owner : string
    repo  : string
    pr_number : number
    github_token : string 
    
    Returns:
    --------
    True/False : boolean
        Returns true if merge successfull else false
    """    
    
    # Construct the API URL for merging the PR
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge'

    # Set up the headers with the GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Set up the data for the merge request
    data = {
        'commit_title': 'Automerge PR',  # You can customize the commit title
        'commit_message': 'Automatically merged by script'  # You can customize the commit message
    }

    # Make the API request to merge the PR
    response = requests.put(url, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        #print(f'PR #{pr_number} successfully merged!')
        return True
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to merge PR. Status code: {response.status_code}, Message: {response.json()["message"]}')
        return False


#parameters
owner = 'vijaikannangit'
repo = 'jenkins-python-script'
pr_number = 3
github_token = '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'
minimum_approvals = 2

pr_eligible = is_pr_eligible(owner, repo, pr_number, github_token)
if pr_eligible=='closed':
    print(f'PR #{pr_number} is already Merged/Closed!')
elif pr_eligible!='open' and pr_eligible!='closed' :
    print(f'The given PR #{pr_number} state is {pr_eligible}. It should be in open state for merging')
elif pr_eligible =='clean':
    print(f"The given pull request is not in mergeable state. Merge state found is {pr_eligible}")
else:
    print(f'PR #{pr_number} Checking Approval...')
    approvers_count = is_pr_approved_min_approvals(owner, repo, pr_number, github_token, minimum_approvals)
    if approvers_count > 1:
        print(f'Number of Approvals for PR #{pr_number} is {approvers_count}')
        print(f'PR #{pr_number} Auto Merging PR ...')
        if automerge_pr(owner, repo, pr_number, github_token):
           print(f'Automerging of PR #{pr_number} successful!')
        else:
           print(f'Automerging of PR #{pr_number} failed.')
    else:
       print(f'PR #{pr_number} does not have sufficient approvals ({approvers_count}). The required minimum number of approvers : {minimum_approvals}')
