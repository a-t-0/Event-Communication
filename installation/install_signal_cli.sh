#!/bin/bash

verify_script_is_ran_from_this_dir() {
    local end_of_path="${PWD:(-12)}"
    if [[ "$end_of_path" != "installation" ]]; then
        exit "The script is not called from the installation directory."
        exit 20
    fi
}
verify_script_is_ran_from_this_dir


yes | sudo apt-get install default-jre
# TODO: verify default-jre is installed correctly, using --version command
yes | sudo apt-get install openjdk-17-jdk
# TODO: verify openjdk-17-jdk is installed correctly, using --version command
# TODO: verify the /usr/lib/jvm/java-1.17.0-openjdk-amd64 dir exists.
export JAVA_HOME=/usr/lib/jvm/java-1.17.0-openjdk-amd64

# Check if repo exists, if not, clone it
SIGNAL_CLI_REPO_NAME="signal-cli"
SIGNAL_CLI_GIT_USERNAME="AsamK"
clone_signal_cli_repo_if_not_exist() {
    local signal_cli_git_username="$1"
    local signal_cli_repo_name="$2"

    if [[ ! -d "$SIGNAL_CLI_REPO_NAME" ]]; then
        echo "$SIGNAL_CLI_REPO_NAME does not yet exists on your filesystem."
        git clone https://github.com/$signal_cli_git_username/$signal_cli_repo_name.git
    else
        echo "$signal_cli_repo_name exists on your filesystem."
    fi
}
clone_signal_cli_repo_if_not_exist "$SIGNAL_CLI_GIT_USERNAME" "$SIGNAL_CLI_REPO_NAME"
# TODO: assert repo exists.



cd signal-cli

build_was_succesfull() {
    local output="$1"
    if [[ "$output" == *"BUILD"* ]] && [[ "$output" == *"SUCCESSFUL"* ]]; then
        echo "Found BUILD and SUCCESSFUL, moving on."
    else
        echo "Error, build was not successful. Output=$output"
    fi
}
output=$(./gradlew build)
build_was_succesfull "$output"
output=$(./gradlew installDist)
build_was_succesfull "$output"
output=$(./gradlew distTar)
build_was_succesfull "$output"
output=$(./gradlew fatJar)
build_was_succesfull "$output"
output=$(./gradlew run --args="--help")
build_was_succesfull "$output"


# TODO: assert dir exists.
cd build/distributions

# Unpack the compressed .tar file to the /opt directory.
# TODO: assert tar file exists.
sudo tar xf signal-cli-0.*.*.tar -C /opt

# Move the unpacked distribution into the /usr/local/bin/ directory
sudo ln -sf /opt/signal-cli-0.*.*/bin/signal-cli /usr/local/bin/

# TODO: verify signal-cli works.
signal_cli_works() {
    local output="$1"
    if [[ "$output" == *"signal-cli"* ]] && [[ "$output" == *"0.10"* ]]; then
        echo "signal-cli works."
    else
        echo "Error, signal-cli does not work. Output=$output"
    fi
}

output=$(signal-cli --version)
signal_cli_works "$output"
