nagios-docker
=============

A Python based Nagios plugin for monitoring docker.

## Requirements

* Python 2.7+
* Nagios 3
* Docker <http://docker.io>

## Usage

This information requires that you already have docker and nagios setup. For
more information on setting up docker, visit
http://www.docker.io/gettingstarted/ and for information setting up nagios,
visit http://nagios.sourceforge.net/docs/3_0/quickstart.html

These instructions were written using the Ubuntu 13.10 default install
directories. Your environment may be different.

1. Get the repository:

```
git clone https://github.com/jharkins/nagios-docker.git
```

2. Copy the docker_socket.py file into nagios plugin directory:

```
cp docker_socket.py /usr/lib/nagios/plugins/docker_socket.py
```

3. Ensure that docker_socket.py is executable:

```
chmod +x /usr/lib/nagios/plugins/docker_socket.py
````

4. Add docker_status command to NRPE config on client host:

Add:

```
command[docker_status]=/usr/lib/nagios/plugins/docker_socket.py
```

to file **/etc/nagios/nrpe.cfg**

5 Add nagios to docker group so the plugin, running as nagios, can access the
docker socket:

```
usermod -a -G docker nagios
```

6. Restart NRPE on client host:

```
service nagios-nrpe-server restart
```

7. Add the docker_status command to the Nagios monitoring server:

Define docker_status command in **/etc/nagios3/objects/commands.cfg**

```
define command{
    command_name    docker_status
    command_line    $USER1$/check_nrpe -H $HOSTADDRESS$ -c docker_status
}
```

8. Add the docker_status check for the client server on the monitoring server:

Add the following to **/etc/nagios3/conf.d/<server>.cfg**:

```
define service {
      use                             generic-service
      host_name                       docker.bitstormtech.com
      service_description             Docker service information
      check_command                   docker_status
}
```

9. Restart Nagios on the monitoring server:

```
service nagios restart
```
