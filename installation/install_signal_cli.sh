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
        exit 5
    fi
}

output=$(signal-cli --version)
signal_cli_works "$output"


ask_yes_no_question() {
    local question="$1"
    while true; do
		read -p "$question (y/n)" yn
		case $yn in
		[Yy]* ) echo "yes"; break;;
		[Nn]* ) echo "no"; break;;
		* ) echo "Please answer yes or no." >&2;;
		esac
	done

}


# Register this computer as sub to your phone.

# Install software that can convert a link into a qr code.
sudo apt-get install -y libqrencode-dev

device_is_connected(){
    local command_output="$1"
    while IFS= read -r line; do
        #echo "... $line ..."
        if [[ "$line" == *"this device"* ]]; then
            echo "Connected"
        fi
    done <<< "$command_output"
}

device_is_registered(){
    local phone_nr="$1"
    # Ask user to get phone out and ready to scan linked device.
    ask_yes_no_question "Will you please open Signal on your phone, go to:Settings>Linked devices>+ and scan the qr code that will appear?"
    device_is_connected="FALSE"

    while [[ "$device_is_connected" == "FALSE" ]]; do
        # Generate the signal-cli registration link and convert it into a qr code, to scan with your phone.
        signal-cli link -n "event-communication" | xargs -L 1 qrencode -o /tmp/qrcode.png & while [ ! -f /tmp/qrcode.png ]; do sleep 1; done; xdg-open /tmp/qrcode.png
        # This is for newer devices, it was not verified:
         # signal-cli link -n "optional device name" | xargs -L 1 qrencode -o /tmp/qrcode.png --level=H -v 10 & while [ ! -f /tmp/qrcode.png ]; do sleep 1; done; xdg-open /tmp/qrcode.png`
        sleep 15
        # Verify device is registered
        connected_devices=$(signal-cli -u $phone_nr listDevices)
        echo "connected_devices=$connected_devices"
        if [[ $(device_is_connected "$connected_devices") == "Connected" ]]; then
		    echo "terminating loop. Signal is connected";
            device_is_connected="TRUE"
		fi
	done
}
read -p "Please enter your phone number in the format <country code><nr>, like +242612345678 " PHONE_NR
echo "PHONE_NR=$PHONE_NR"
device_is_registered "$PHONE_NR"
