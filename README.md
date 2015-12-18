# vmpooler_client.py
The "vmpooler_client.py" script provides the ability to manage vmpooler
resources in the vcloud. Currently the script supports grabbing
a new VM for testing and handing a VM back to the pooler to be
destroyed.

To get help on the command-line for the script use the command:

```
vmpooler_client.py -h
```

### Quickstart

```
# Create a token (only on first run)
$ ./vmpooler_client.py token create
Please provide LDAP credentials for the VM pooler

Username: bob.smith
Password:

Token: <token>

# List available templates
$ ./vmpooler_client.py vm list redhat
redhat-4-x86_64
redhat-5-i386
redhat-5-x86_64
redhat-6-i386
redhat-6-x86_64
redhat-7-x86_64

# Grab a VM
$ ./vmpooler_client.py vm get redhat-6-x86_64
Hostname: h2qbe7c29ix2w1r

# Login and do work
$ ssh root@h2qbe7c29ix2w1r

# Logout

# Give vm back to the pool
$ ./vmpooler_client.py vm destroy h2qbe7c29ix2w1r
```


### Examples
`vmpooler_client.py` is separated into a few subcommands:
```
vmpooler_client.py
	* vm
		* list
		* get
		* destroy
		* destroy_all
		* info
		* running
	* lifetime
		* get
		* extend
		* set
	* token
		* create
		* validate
		* revoke
	* config
	    * get
	    * set
	    * list
	    * unset
```

Help is available for each subcommand by appending `-h` to the command:
```
vmpooler_client.py lifetime set -h
```

#### List vmpooler templates
This will list all the available templates.

**Usage**
```
vmpooler_client.py vm list
```

#### Filter the list vmpooler templates
Filter available templates via a fuzzy matching pattern.

**Usage**
```
vmpooler_client.py vm list PATTERN
```

**Example**
```
vmpooler_client.py vm list win
```

#### Get a VM from the vmpooler
It is required that you know what the template names are for the
vmpooler.

**Usage**
```
vmpooler_client.py vm get TEMPLATE_NAME
```

**Example**
```
vmpooler_client.py vm get ubuntu-1404-x86_64
```

#### List all of your running VMs
This gives you a concise list of what VMs you have running

**Usage**
```
vmpooler_client.py vm running
```

**Example Output**
```
l2l7jdlpt6xlptq | Running: 4.27 hours | centos-6-i386
etcgjzxks2vtw9t | Running: 0.15 hours | centos-5-i386
```

#### Hand a VM back to the vmpooler for destruction
It is required that you know what the hostname is for the VM you want to
destroy.

**Usage**
```
vmpooler_client.py vm destroy VM_NAME
```

**Example**
```
vmpooler_client.py vm destroy skj3k4hahdk
```

#### Hand all active VMs back to the vmpooler for destruction
Be careful, this will destroy every active VM associate with your token

**Usage**
```
vmpooler_client.py vm destroy_all
```

**Example Output**
```
Destroying etcgjzxks2vtw9t
Destroying l2l7jdlpt6xlptq
```

#### Get the time to live for a VM in the vmpooler

**Usage**
```
vmpooler_client.py lifetime get VM_NAME
```

**Example**
```
vmpooler_client.py lifetime get skj3k4hahdk
```

#### Extend the time to live for a VM in the vmpooler
This command will add a certain number of hours to the lifetime of a VM

**Usage**
```
vmpooler_client.py lifetime extend VM_NAME LIFETIME
```

**Example**
```
vmpooler_client.py lifetime extend skj3k4hahdk 2
> Lifetime extended to 10 hours
```

#### Set the total time to live for a VM in the vmpooler to a certain number of hours
This command will overwrite the time to live for a VM

**Usage**
```
vmpooler_client.py lifetime set VM_NAME LIFETIME
```

**Example**
```
vmpooler_client.py lifetime set skj3k4hahdk 24
```

#### Get information on a VM in the vmpooler
This will work on running and destroyed VMs in the vmpooler.

**Usage**
```
vmpooler_client.py vm info VM_NAME
```

**Example**
```
vmpooler_client.py vm info skj3k4hahdk
```

#### Create an authorization token for use with the vmpooler
WARNING! Know what you're doing before using this function!

**Usage**
```
vmpooler_client.py token create
```

#### Revoke an authorization token
WARNING! Know what you're doing before using this function!

**Usage**
```
vmpooler_client.py token revoke TOKEN
```

**Example**
```
vmpooler_client.py token revoke sfn3h65earxah6ar9aal3oac2pfx9817
```

#### Verify that an authorization token is valid
WARNING! Know what you're doing before using this function!

**Usage**
```
vmpooler_client.py token validate TOKEN
```

**Example**
```
vmpooler_client.py token validate sfn3h65earxah6ar9aal3oac2pfx9817
```

#### Read a config setting
**Usage**
```
vmpooler_client.py config get SETTING_NAME
```

**Example**
```
vmpooler_client.py config get username
```

#### Modify/create a config setting
Modify an existing setting or create add a new setting if it doesn't exist yet.

**Usage**
```
vmpooler_client.py config set SETTING_NAME VALUE
```

**Examples**
```
vmpooler_client.py config set username bob.smith
vmpooler_client.py config set a_new_setting some_value
```

#### Remove a config setting
**Usage**
```
vmpooler_client.py config unset SETTING_NAME
```

**Example**
```
vmpooler_client.py config unset auth_token
```

#### List all config settings
Print all the settings in the config file
**Usage**
```
vmpooler_client.py config list
```