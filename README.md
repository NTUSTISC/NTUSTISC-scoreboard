# NTUSTISC-scoreboard

## Server
### Start Server
- `bash docker.sh`

### Server Struction
- docker
	- NTUSTISC (network)
		- scoreboard (container)
		- postgresql (container)

### Settings Flags
- CTF
	- Whether CTF is ongoing
- CTF_NAME
	- This CTF's name. The filename will be stored CTF data.
- SHELL
	- Whether run [postgresql.py](postgresql.py) to create initialization objects

## Feature
### Team and CTF
- if not settings.CTF
	- login @user
	- submit @user flag
- else
	- can register and login with team or username
	- enter only username
		- login with @user
		- submit @user flag
	- enter teamname and username
		- create team if the teamname is not exist
		- login with user@team if user@team exist
		- submit @team flag
	- enter teamname, token and username
		- login with user@team if user@team exist
		- login with user@team if team@token paired and len(user@team) < 4
		- submit @team flag

### CTF finished
- `curl /ctf_finish` when not settings.CTF
	- with open(settings.BASE_DIR + "/" + settings.CTF_NAME, "w") as file
		- save all about serialize ctf objects

### Score
- Score Base: 500
- Minimum Score: 100
- Transform From (sigmoid function)[https://en.wikipedia.org/wiki/Sigmoid_function]
	- Function Revise: `2 / (1 + exp(3 * x))`
- Function
	- max(Base * Revise, Minimum)
	- max(int(1000 / (1 + exp(3 * x))), 100)
