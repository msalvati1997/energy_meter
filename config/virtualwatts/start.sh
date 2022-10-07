sudo docker run -t --net=host -v $(pwd)/config_file.json:/config_file.json powerapi/virtualwatts --config-file /config_file.json
