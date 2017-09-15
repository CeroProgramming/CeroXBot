#!/bin/bash

if ! id -u discordbot > /dev/null 2>&1; then
  echo "The user dicordbot doesn't exist. Creating.."
  sudo su -c "adduser discordbot --shell /bin/bash --home /srv/discordbots --disabled-password --disabled-login --gecos 'Discordbot User,None,None,None'"
else
  if [ ! -d "/srv/discordbots" ]; then
    echo "The user dicordbot already exist, but the main directory doesn't. Creating.."
    sudo mkdir /srv/discordbots
    sudo chown discordbot:discordbot /srv/discordbots
  else
    echo "The user dicordbot already exist. Continuing.."
  fi
fi

if [ ! -d "/srv/discordbots/NextBot" ]; then
  echo "Creating the nextbot directory (/srv/discordbots/NextBot).."
  sudo -u discordbot mkdir /srv/discordbots/NextBot
fi

echo "Moving all data to main directory.."
sudo mv * /srv/discordbots/NextBot

echo "Changing owner of the data to discordbot.."
sudo chown discordbot:discordbot -R /srv/discordbots/NextBot


if [ ! -d "/etc/conf.d/" ]; then
  echo "The directory /etc/conf.d doesn't exist. Creating.."
  sudo mkdir /etc/conf.d/
else
  echo "The directory /etc/conf.d already exist. Skipping.."
fi

echo "Copying important service files.."
sudo cp /srv/discordbots/NextBot/setup/nextbot.conf /etc/conf.d/nextbot
sudo chmod 755 /etc/conf.d/nextbot
sudo cp /srv/discordbots/NextBot/setup/nextbot.sh /usr/bin/nextbot
sudo chown discordbot:discordbot /usr/bin/nextbot
sudo chmod 755 /usr/bin/nextbot
if [ ! -d "/usr/lib/systemd/system" ]; then
  sudo cp /srv/discordbots/NextBot/setup/nextbot.service /etc/systemd/system/nextbot.service
  sudo chmod 755 /etc/systemd/system/nextbot.service
else
  sudo cp /srv/discordbots/NextBot/setup/nextbot.service /usr/lib/systemd/system/nextbot.service
  sudo chmod 755 /usr/lib/systemd/system/nextbot.service
fi
systemctl enable nextbot.service
service nextbot start
