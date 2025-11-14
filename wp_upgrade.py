#!/usr/bin/env python3
import os
import subprocess
import logging
import argparse

# Configure logging (Store logs system-wide)
LOG_FILE = "/var/log/wp_upgrade.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Common directories where WordPress installations might be found. Change the path of your WP here
COMMON_DIRS = [
    "/var/web", "/www/html", "/new/", "/home" 
]

def find_wordpress_sites():
    """Find WordPress installations across the server"""
    wp_sites = []
    for base_dir in COMMON_DIRS:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            if 'wp-config.php' in files:
                wp_sites.append(root)
    return wp_sites

def run_wp_cli_command(site_path, command):
    """Run WP-CLI commands in the given WordPress site directory with --allow-root"""
    full_command = f"wp {command} --path={site_path} --allow-root"
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"✔ Successfully ran: {full_command}")
        logging.info(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error running: {full_command}")
        logging.error(e.stderr)
        return None

def upgrade_wordpress(site_path, options):
    """
    Upgrade WordPress core, plugins, themes, and WooCommerce database
    according to selected options.
    """
    logging.info(f"🔄 Upgrading WordPress site at {site_path}")

    # Core update
    if options.core:
        run_wp_cli_command(site_path, "core update")

    # Core DB update
    if options.db:
        run_wp_cli_command(site_path, "core update-db")

    # Plugins
    if options.plugins:
        run_wp_cli_command(site_path, "plugin update --all")

    # Themes
    if options.themes:
        run_wp_cli_command(site_path, "theme update --all")

    # WooCommerce DB
    if options.wc_db:
        run_wp_cli_command(site_path, "wc update")

    logging.info(f"✅ Upgrade completed for {site_path}\n" + "="*50)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run WP-CLI upgrades on all detected WordPress sites."
    )

    parser.add_argument(
        "--core",
        action="store_true",
        help="Update WordPress core"
    )
    parser.add_argument(
        "--db",
        action="store_true",
        help="Run WordPress core database update"
    )
    parser.add_argument(
        "--plugins",
        action="store_true",
        help="Update all plugins"
    )
    parser.add_argument(
        "--themes",
        action="store_true",
        help="Update all themes"
    )
    parser.add_argument(
        "--wc-db",
        dest="wc_db",
        action="store_true",
        help="Run WooCommerce database update (wc update)"
    )
    parser.add_argument(
        "--path",
        help="Limit upgrades to a specific WordPress path (or prefix)",
        default=None,
    )

    return parser.parse_args()

def main():
    options = parse_args()

    # If no specific option is given, run everything (backward compatible)
    if not any([options.core, options.db, options.plugins, options.themes, options.wc_db]):
        options.core = True
        options.db = True
        options.plugins = True
        options.themes = True
        options.wc_db = True

    logging.info("🚀 Starting sitewide WordPress upgrade process...")

    wordpress_sites = find_wordpress_sites()

    if options.path:
        wordpress_sites = [
            s for s in wordpress_sites
            if s == options.path or s.startswith(options.path.rstrip("/"))
        ]

    if not wordpress_sites:
        logging.warning("⚠ No WordPress sites found!")
        return

    for site in wordpress_sites:
        upgrade_wordpress(site, options)

    logging.info("🎉 All selected upgrades completed successfully.")

if __name__ == "__main__":
    main()
