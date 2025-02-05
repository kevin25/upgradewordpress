import os
import subprocess
import logging

# Configure logging (Store logs system-wide)
LOG_FILE = "/var/log/wp_upgrade.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Common directories where WordPress installations might be found
COMMON_DIRS = [
    "/var/web", "/www/html", "/new/", "/home"
]

def find_wordpress_sites():
    """Find WordPress installations across the server"""
    wp_sites = []
    for base_dir in COMMON_DIRS:
        for root, dirs, files in os.walk(base_dir):
            if 'wp-config.php' in files:
                wp_sites.append(root)
    return wp_sites

def run_wp_cli_command(site_path, command):
    """Run WP-CLI commands in the given WordPress site directory with --allow-root"""
    full_command = f"wp {command} --path={site_path} --allow-root"
    try:
        result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"✔ Successfully ran: {full_command}")
        logging.info(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error running: {full_command}")
        logging.error(e.stderr)
        return None

def upgrade_wordpress(site_path):
    """Upgrade WordPress core, plugins, themes, and WooCommerce database"""
    logging.info(f"🔄 Upgrading WordPress site at {site_path}")

    # Upgrade WordPress Core
    run_wp_cli_command(site_path, "core update")

    # Upgrade Database
    run_wp_cli_command(site_path, "core update-db")

    # Upgrade Plugins
    run_wp_cli_command(site_path, "plugin update --all")

    # Upgrade Themes
    run_wp_cli_command(site_path, "theme update --all")

    # Upgrade WooCommerce Database (if WooCommerce is installed)
    run_wp_cli_command(site_path, "wc update")  # For WooCommerce database update

    logging.info(f"✅ Upgrade completed for {site_path}\n" + "="*50)

def main():
    logging.info("🚀 Starting sitewide WordPress upgrade process...")
    
    wordpress_sites = find_wordpress_sites()
    
    if not wordpress_sites:
        logging.warning("⚠ No WordPress sites found!")
        return

    for site in wordpress_sites:
        upgrade_wordpress(site)

    logging.info("🎉 All WordPress sites upgraded successfully.")

if __name__ == "__main__":
    main()
