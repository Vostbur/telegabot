Install as a service
==============

Exec as root or with sudo:

    cat > /etc/systemd/system/bot.service << EOF
    
    [Service]
    Environment="BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    Environment="TELEGRAM_ID=xxxxxxx"
    WorkingDirectory=/home/user
    User=user
    ExecStart=/usr/bin/python3 bot.py
    
    [Install]
    WantedBy=multi-user.target
    EOF

    systemctl daemon-reload
    systemctl enable bot
    systemctl start bot
    systemctl status bot


Remove service
-------------------

    systemctl stop bot
    systemctl disable bot
    rm /etc/systemd/system/bot.service
    systemctl daemon-reload
