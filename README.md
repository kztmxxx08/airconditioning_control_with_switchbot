# Air conditioning controller with switchbot
このプロジェクトはpythonとSwitchbotを用いて空調のコントロールを行います。

This project uses python and Switchbot to control air conditioning.

## 概要：Description
このプロジェクトは取得した気温および湿度からエアコンおよび加湿器を稼働させます。
電源オフの時間になった際は、エアコンと加湿器の電源オフを実行します。
気温と湿度はMySQL(MariaDB)のデータベースから読み込んだ値を用います。

現時点では気温、湿度の取得およびエアコン、加湿器の電源オフのみ実装されています。

This project will run the air conditioner and humidifier based on the temperature and humidity obtained.
When it is time to turn off the power, it will turn off the air conditioner and humidifier.
The temperature and humidity values are read from a MySQL (MariaDB) database.

At this time, only the acquisition of temperature and humidity and the turning off of the air conditioner and humidifier are implemented.

## 使用方法：Usage
### Define environment
Create an .env file in the project directory and set the following environment variables

```
# Switch bot information
export SWITCHBOT_DEVELOPER_TOKEN="<Switch bot developer token>"
export SWITCHBOT_DEVICE_ID="Switch bot device id"
# MySQL information
export MYSQL_HOST="<MYSQL HOST IP or NAME>"
export MYSQL_USER="<MYSQL USERNAME>"
export MYSQL_PASSWORD="<MYSQL PASSWORD>"
export MYSQL_DB_NAME="<MYSQL DB NAME>"
export MYSQL_PORT="3306"
```

### Define settings.yaml
settings.yamlを編集します。
TableNameは温度と湿度のテーブル名を指定してください。
poweroff_hour_minutesは家電の電源を切る時間を記載してください。（例として23時55分としています。）

TableName should be the name of the temperature and humidity table.
poweroff_hour_minutes should be the time when the appliances are turned off. (For example, 23:55 is used.)

### execution
```
$ python control.py
```
* 必要な場合はcronなどを用いて実行する。
* If necessary, run it by cron or other means.

## Requirement
* python3
* logging
* mysqlclient
* python-dotenv
* PyYAML
* requests


## Author
Tomoki.H
