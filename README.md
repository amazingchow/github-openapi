# github-openapi

## Get Started

### Prerequisites

* Linux or MacOS
* Installed python 3.7 or higher

### Installation

#### Clone

* Clone this repo to your local machine using https://github.com/amazingchow/github-openapi.git.

#### Setup

```shell
cd /path/to/github-openapi
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## CRUD Operations for Your Personal GitHub Space

* read operations

- [x] list all repositories [list_repos.py]
- [x] list all starred repositories [list_stars.py]
- [x] list all followers [list_followers.py]
- [x] list all followings [list_followings.py]

* write operations

- [x] follow one person [follow.py]
- [x] unfollow one person [unfollow.py]
- [x] star one repository [star.py]
- [x] unstar one repository [unstar.py]
- [x] fork one repository [fork.py]
- [x] delete one repository [delete.py]
- [x] push one commit  [commit.py]

## References

* [GitHub REST API v3](https://developer.github.com/v3/)

## Contributing

### Step 1

* 🍴 Fork this repo!

### Step 2

* 🔨 HACK AWAY!

### Step 3

* 🔃 Create a new PR using https://github.com/amazingchow/github-openapi/compare!

## Support

* Reach out to me at <jianzhou42@163.com>.

## License

* This project is licensed under the MIT License - see the **[MIT license](http://opensource.org/licenses/mit-license.php)** for details.
