# Onlooker

Onlooker is a Dockerized Python application that monitors a remote FTP server for new files and automatically downloads new files to a local storage location. The primary purpose of the container is to serve as a proof-of-concept for custom Dockerized applications deployed on Cisco Catalyst 9000 and Nexus 9000 platforms.

## Usage

```
docker create \
--name=onlooker \
-e FTP_IP=<ftp-server-ip-or-fqdn> \
-e FTP_USER=<ftp-server-username> \
-e FTP_PASS=<ftp-server-password> \
-e DEBUG=<1/0>
-v <local-storage>:/storage
chrisjhart/onlooker
```

If desired, the user may also utilize Docker Compose to use this application. The docker-compose.yml file in this repository may be used as an example. For more information about how to utilize Docker Compose on the Cisco NX-OS, refer to the Cisco documentation for [Installing Docker Compose in the NX-OS Bash Shell](https://www.cisco.com/c/en/us/support/docs/switches/nexus-9000-series-switches/213961-install-docker-compose-in-nx-os-bash-she.html).

## Parameters

* `-e FTP_IP` - A value representing the IP address or Fully Qualified Domain Name (FQDN) of the FTP server that this application should monitor.
* `-e FTP_USER` - A value representing the username to be used to log into the FTP server defined by the `FTP_IP` environment variable.
* `-e FTP_PASS` - A value representing the password of the user account defined by the `FTP_USER` environment variable used to log into the FTP server defined by the `FTP_IP` environment variable.
* `-e DEBUG` - When set to `1`, enables debug logging to the container console. This should be used for troubleshooting - it is not recommended to enable this in a production environmnent.
* `-v <local-storage>:/storage` - Mounts the filepath defined by `<local-storage>` inside the Docker container in the `/storage` directory. This is the filepath where new files detected on the remote FTP server will be downloaded to. 
  * On Nexus 9000 devices, `<local-storage>` should typically be set to `/bootflash`

## License

This project is licensed under the terms of the Cisco Sample Code License. Please refer to the LICENSE.md file in this repository for more information, or view the license [here](https://developer.cisco.com/docs/licenses/#!cisco-sample-code-license/cisco-sample-code-license).