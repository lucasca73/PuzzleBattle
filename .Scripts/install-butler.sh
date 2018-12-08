#! /bin/sh

# apt-get update && apt-get install unzip

# -L follows redirects
# -O specifies output name
if [ "$1" = "linux" ]; then
    curl -L -o butler.zip https://broth.itch.ovh/butler/linux-amd64/LATEST/archive/default
else
    curl -L -o butler.zip https://broth.itch.ovh/butler/darwin-amd64/LATEST/archive/default
fi
unzip butler.zip
# GNU unzip tends to not set the executable bit even though it's set in the .zip
chmod a+x ./butler
# just a sanity check run (and also helpful in case you're sharing CI logs)
./butler -V
./butler login