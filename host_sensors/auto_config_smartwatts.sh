#!/usr/bin/env bash

maxfrequency=$(lscpu -b -p=MAXMHZ | tail -n -1| cut -d , -f 1)
minfrequency=$(lscpu -b -p=MINMHZ | tail -n -1 | cut -d , -f 1)
basefrequency=$(lscpu | grep "Model name" | cut -d @ -f 2 | cut -d G -f 1)
basefrequency=$(expr ${basefrequency}\*1000 | bc | cut -d . -f 1)


echo "
{
  \"verbose\": false,
  \"stream\": true,
  \"input\": {
    \"puller\": {
      \"type\": \"mongodb\",
      \"uri\": \"mongodb://127.0.0.1\",
      \"db\": \"powerapi\",
      \"collection\": \"hwpcsensor\"
    }
  },
  \"output\": {
    \"pusher_power\": {
      \"type\": \"influxdb\",
      \"model\": \"PowerReport\",
      \"uri\": \"127.0.0.1\",
      \"port\": 8086,
      \"db\": \"powerapi_formula\",
      \"collection\": \"smartwatts\"
    }
  },
  \"cpu-frequency-base\": $basefrequency,
  \"cpu-frequency-min\": $minfrequency,
  \"cpu-frequency-max\": $maxfrequency,
  \"real-time-mode\": true,
  \"learn-min-samples-required\": 10,
  \"learn-history-window-size\": 60,
  \"disable-cpu-formula\": false,
  \"cpu-error-threshold\": 2.0,
  \"disable-dram-formula\": true,
  \"sensor-report-sampling-interval\": 1000
}
" > ./host_sensors/smartwatts_config.json

