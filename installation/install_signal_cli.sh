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


./gradlew build
# TODO: verify output contains "build successful"
./gradlew installDist
# TODO: verify output contains "build successful"
./gradlew distTar
# TODO: verify output contains "build successful"
./gradlew fatJar
# TODO: verify output contains "build successful"
./gradlew run --args="--help"
# TODO: verify output contains "BUILD successful"
exit 34
cd build/distributions
# Unpack the compressed .tar file to the /opt directory.
sudo tar xf signal-cli-0.*.*.tar -C /opt
# Move the unpacked distribution into the /usr/local/bin/ directory
sudo ln -sf /opt/signal-cli-0.*.*/bin/signal-cli /usr/local/bin/
