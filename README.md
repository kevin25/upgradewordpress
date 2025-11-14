How to use it

Run everything (same behavior as your original script):

python3 wp_upgrade.py

Only upgrade core:

python3 wp_upgrade.py --core


Only upgrade plugins:

python3 wp_upgrade.py --plugins


Only upgrade themes:

python3 wp_upgrade.py --themes


Core + DB + plugins (for example):

python3 wp_upgrade.py --core --db --plugins


Only WooCommerce DB:

python3 wp_upgrade.py --wc-db


Limit to a specific site path:

python3 wp_upgrade.py --core --plugins --path /mnt/home/example.com/public_html


If you want an interactive “choose 1–5” menu version instead of CLI flags, I can rewrite it that way too.

0 0 * * 0 python3 /path/to/wp_upgrade.py
