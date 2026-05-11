# Troubleshooting Odoo Docker Setup

## Internal Server Error (500) on First Run

### Symptom
When accessing `http://localhost:8029` (or your configured port), you see an "Internal Server Error" page.
The logs (`docker logs odoo-web-1`) show an error like:
`ERROR ? odoo.modules.loading: Database odoo not initialized, you can force it with -i base`
or
`KeyError: 'ir.http'`

### Cause
The Postgres container successfully created the database (e.g., `odoo`), but the Odoo server has not yet installed the base modules and tables into that database. Odoo 17 and above may throw a 500 error instead of showing the database manager if it's already "bound" to a specific database name.

### Solution
You need to manually trigger the base module installation. Run the following command in your project directory:

```bash
docker compose run --rm web odoo -i base --stop-after-init
```

Once the command finishes (it will show `Modules loaded` and then exit), restart your containers:

```bash
docker compose up -d
```

## Permission Denied on Config Folder
If you see `grep: /etc/odoo/odoo.conf: No such file or directory` or permission errors in the logs:
1. Ensure the `config` folder exists locally.
2. If Docker created the folder as `root`, change the ownership back to your user:
   ```bash
   sudo chown -R $USER:$USER config/
   ```

## Custom Module Not Found in Apps List

### Symptom
You added a module in `custom_addons/`, but it doesn't appear in the Odoo Apps list even after searching.

### Cause
Odoo must be explicitly told to look in the `/mnt/extra-addons` folder via the `addons_path` configuration. If using Odoo 19+, environment variables like `ADDONS_PATH` might be ignored if a config file is present or if the entrypoint isn't configured for it.

### Solution
1. Ensure your `docker-compose.yml` mounts the volume:
   ```yaml
   volumes:
     - ./custom_addons:/mnt/extra-addons
     - ./config_odoo:/etc/odoo
   ```
2. Check `config_odoo/odoo.conf` and ensure the `addons_path` includes `/mnt/extra-addons`:
   ```ini
   [options]
   addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
   ```
3. In the Odoo UI:
   - Go to **Apps**.
   - Click **Update Apps List** (Mettre à jour la liste des Apps).
   - Search for your module (remove the "Apps" filter if necessary).

## Permission Denied in Volumes (UID Mismatch)

### Symptom
Logs show: `AssertionError: ... directory is not writable` or `Permission denied` inside `/var/lib/odoo`.

### Cause
Different Odoo Docker images may run as different User IDs (UID).
- Odoo 17.0 often uses UID `101`.
- Odoo 19 (master) may use UID `100`.
If you switch versions, the files in the volume might be owned by the previous UID.

### Solution
Fix the ownership inside the running container:
```bash
docker exec -u root odoo-web-1 chown -R odoo:odoo /var/lib/odoo
docker compose restart web
```
