# A simple way to update Flask Heroku's static files.

# ----------------------
#  Useful variables
# ----------------------
NORM=\033[0m
BOLD=\033[1m
CHECK=\033[32m✔\033[39m
port=5000


# ----------------------
#  Default build
# ----------------------
build:
	@echo "\n⚡  ${BOLD}This might take a minute${NORM}  ⚡\n"
	@make clone
	@make update
	@make js
	@rm -rf {bootstrap,update}
	@echo "\n⚡  ${BOLD}Successfully updated${NORM}  ⚡\n"

