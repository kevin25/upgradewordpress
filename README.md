# upgradewordpress
Python script upgrades WordPress and WooCommerce

To automate weekly updates, add a cron job:

sudo crontab -e

Add the following line to run every Sunday at midnight:

0 0 * * 0 python3 /path/to/upgrade_wordpress.py
