# config. We could make this an option to the job. Or be project specific.
U3D_INSTALL_ARGS=-p Unity,Linux,Windows

# install or update u3d if it isn't already present
if [[ ! `which u3d` ]]; then 
  gem install u3d
else
  gem update u3d
fi

echo "${U3D_INSTALL_ARGS}"

# display whether or not the slave has credentials stored
u3d credentials check

# fetch the password for the slave from the credentials
PASS_KEY=U3D_PASSWORD_${NODE_NAME}
echo "PASS KEY: ${PASS_KEY}"
export U3D_PASSWORD=${!PASS_KEY}

# install the specified version with the specified arguments
u3d install --trace --verbose $U3D_VERSION $U3D_INSTALL_ARGS 
u3d list