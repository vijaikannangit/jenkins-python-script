import requests

def is_pr_merged(owner, repo, pr_number, github_token):
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
        # Check the 'merged' field in the response JSON
        print (response.json()['state'])

        # print (response.json()['opened'])
        return response.json()['merged']
    
    else:
        # Print an error message if the request was not successful
        print(f'Error: Unable to fetch PR information. Status code: {response.status_code}')
        return False

owner = 'vijaikannangit'
repo = 'jenkins-python-script'
pr_number = 1 
github_token = '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'
minimum_approvals = 2

if is_pr_merged(owner, repo, pr_number, github_token):
    print(f'PR #{pr_number} is merged!')
else:
    print(f'PR #{pr_number} is not merged or an error occurred.')
