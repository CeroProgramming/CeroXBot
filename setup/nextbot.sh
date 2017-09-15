#!/bin/bash

# The actual program name
declare -r myname="nextbot"
declare -r botname="nextbot"

# General rule for the variable-naming-schema:
# Variables in capital letters may be passed through the command line others not.
# Avoid altering any of those later in the code since they may be readonly (IDLE_SERVER is an exception!)

# You may use this script for any game server of your choice, just alter the config file
[[ ! -z "${SERVER_ROOT}" ]]  && declare -r SERVER_ROOT=${SERVER_ROOT}   || SERVER_ROOT="/srv/discordbots/NextBot"
[[ ! -z "${BOT_USER}" ]]    && declare -r BOT_USER=${BOT_USER}       || BOT_USER="discordbot"
[[ ! -z "${MAIN_EXECUTABLE}" ]] && declare -r MAIN_EXECUTABLE=${MAIN_EXECUTABLE} || MAIN_EXECUTABLE="run.sh"
[[ ! -z "${SESSION_NAME}" ]] && declare -r SESSION_NAME=${SESSION_NAME} || SESSION_NAME="${botname}"

# Command and parameter declaration with which to start the server
[[ ! -z "${SERVER_START_CMD}" ]] && declare -r SERVER_START_CMD=${SERVER_START_CMD} || SERVER_START_CMD="./${MAIN_EXECUTABLE}"

# Variables passed over the command line will always override the one from a config file
source /etc/conf.d/"${botname}" 2>/dev/null || >&2 echo "Could not source /etc/conf.d/${botname}"


# Strictly disallow uninitialized Variables
set -u
# Exit if a single command breaks and its failure is not handled accordingly
set -e

# Check whether sudo is needed at all
if [[ "$(whoami)" == "${BOT_USER}" ]]; then
	SUDO_CMD=""
else
	SUDO_CMD="sudo -u ${BOT_USER}"
fi

# Choose which flavor of netcat is to be used
if which netcat &> /dev/null; then
	NETCAT_CMD="netcat"
elif which ncat &> /dev/null; then
	NETCAT_CMD="ncat"
else
	NETCAT_CMD=""
fi

# Check for sudo rigths
if [[ "$(${SUDO_CMD} whoami)" != "${BOT_USER}" ]]; then
	>&2 echo -e "You have \e[39;1mno permission\e[0m to run commands as $BOT_USER user."
	exit 21
fi

bot_command() {
	if [[ -z "${return_stdout:-}" ]]; then
		${SUDO_CMD} screen -S "${SESSION_NAME}" -X stuff "$(printf "%s\r" "$*")"
	else
		${SUDO_CMD} screen -S "${SESSION_NAME}" -X log on
		${SUDO_CMD} screen -S "${SESSION_NAME}" -X stuff "$(printf "%s\r" "$*")"
		sleep "${sleep_time:-0.3}"
		${SUDO_CMD} screen -S "${SESSION_NAME}" -X log off
	fi
}

server_start() {
	if ${SUDO_CMD} screen -S "${SESSION_NAME}" -Q select . > /dev/null; then
		echo "A screen ${SESSION_NAME} session is already running. Please close it first."
	else
		echo -en "Starting server..."
		${SUDO_CMD} screen -dmS "${SESSION_NAME}" /bin/bash -c "cd '${SERVER_ROOT}'; ${SERVER_START_CMD}"
		echo -e "\e[39;1m done\e[0m"
	fi

}

server_stop() {
	if ${SUDO_CMD} screen -S "${SESSION_NAME}" -Q select . > /dev/null; then

		for i in {1..100}; do
			if ! ${SUDO_CMD} screen -S "${SESSION_NAME}" -Q select . > /dev/null; then
				echo -e "\e[39;1m done\e[0m"
				break
			fi
			[[ $i -eq 100 ]] && echo -e "\e[39;1m timed out\e[0m"
			sleep 0.1
		done
	else
		echo "The corresponding screen session for ${SESSION_NAME} was already dead."
	fi
}

server_status() {
	# Print status information for the server
	if ${SUDO_CMD} screen -S "${SESSION_NAME}" -Q select . > /dev/null; then
		echo -e "Status:\e[39;1m running\e[0m"

		# Calculating memory usage
		for p in $(${SUDO_CMD} pgrep -f "${MAIN_EXECUTABLE}"); do
			ps -p"${p}" -O rss | tail -n 1;
		done | gawk '{ count ++; sum += $2 }; END {count --; print "Number of processes =", count, "(screen, bash,", count-2, "x server)"; print "Total memory usage =", sum/1024, "MB" ;};'
	else
		echo -e "Status:\e[39;1m stopped\e[0m"
	fi
}

# Restart the complete server by shutting it down and starting it again
server_restart() {
	if ${SUDO_CMD} screen -S "${SESSION_NAME}" -Q select . > /dev/null; then
		server_stop
		server_start
	else
		server_start
	fi
}

# Help function, no arguments required
help() {
	cat <<-EOF
	This script was design to easily control any ${botname} server. Quite every parameter for a given
	${botname} server derivative can be altered by editing the variables in the configuration file.

	Usage: ${myname} {start|stop|status}
	    start                Start the ${botname} server
	    stop                 Stop the ${botname} server
	    restart              Restart the ${botname} server
	    status               Print some status information

	Copyright (c) Gordian Edenhofer <gordian.edenhofer@gmail.com>
	EOF
}

case "${1:-}" in
	start)
	server_start
	;;

	stop)
	server_stop
	;;

	status)
	server_status
	;;

	restart)
	server_restart
	;;

	console)
	server_console
	;;

	-h|--help)
	help
	exit 0
	;;

	*)
	help
	exit 1
	;;
esac

exit 0
