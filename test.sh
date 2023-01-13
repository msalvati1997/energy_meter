sudo ./host_sensors/auto_config_hwpc.sh
sudo ./host_sensors/auto_config_smartwatts.sh
sudo docker compose -f host_sensors/docker-compose.yaml down -d
sudo docker compose -f test/docker-compose.yaml down -d

