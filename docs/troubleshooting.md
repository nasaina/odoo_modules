# Troubleshooting — Odoo Docker Setup

## Internal Server Error (500) on First Run

### Symptom
Accessing `http://localhost:8029` (or your configured port) shows an "Internal Server Error" page.
The logs (`docker logs odoo-web-1`) show:
`ERROR ? odoo.modules.loading: Database odoo not initialized, you can force it with -i base`
or
`KeyError: 'ir.http'`

### Cause
The Postgres container successfully created the database, but Odoo has not yet installed the base modules and tables into it. Odoo 17 and above may throw a 500 error instead of showing the database manager when it is already bound to a specific database name.

### Solution
Manually trigger the base module installation:

```bash
docker compose run --rm web odoo -i base --stop-after-init
```

Once the command finishes (you will see `Modules loaded` and then it exits), restart your containers:

```bash
docker compose up -d
```

Or simply run:

```bash
make re
```

## Permission Denied on Config Folder
If you see `grep: /etc/odoo/odoo.conf: No such file or directory` or permission errors in the logs:
1. Make sure the `config_odoo` folder exists locally.
2. If Docker created the folder as `root`, change ownership back to your user:
   ```bash
   sudo chown -R $USER:$USER config_odoo/
   ```

## Custom Module Not Found in Apps List

### Symptom
You added a module in `custom_addons/`, but it does not appear in the Odoo Apps list even after searching.

### Cause
Odoo must be explicitly told to look in `/mnt/extra-addons` via the `addons_path` configuration. If using Odoo 19+, environment variables like `ADDONS_PATH` may be ignored if a config file is present or if the entrypoint is not configured for it.

### Solution
1. Ensure your `docker-compose.yml` mounts the volume:
   ```yaml
   volumes:
     - ./custom_addons:/mnt/extra-addons
     - ./config_odoo:/etc/odoo
   ```
2. Check `config_odoo/odoo.conf` and ensure `addons_path` includes `/mnt/extra-addons`:
   ```ini
   [options]
   addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
   ```
3. In the Odoo UI:
   - Go to **Apps**.
   - Click **Update Apps List**.
   - Search for your module (remove the "Apps" filter if necessary).

## Permission Denied in Volumes (UID Mismatch)

### Symptom
Logs show: `AssertionError: ... directory is not writable` or `Permission denied` inside `/var/lib/odoo`.

### Cause
Different Odoo Docker images may run as different User IDs (UID).
- Odoo 17.0 often uses UID `101`.
- Odoo 19 may use UID `100`.
Switching versions can leave files in the volume owned by the previous UID.

### Solution
Fix ownership inside the running container:
```bash
docker exec -u root odoo-web-1 chown -R odoo:odoo /var/lib/odoo
docker compose restart web
```

## Odoo Version Upgrade (e.g. 17 → 19)

### Symptom
Running `odoo -u all` fails with:
`psycopg2.errors.InvalidTextRepresentation: invalid input syntax for type json`

### Cause
Direct major version upgrades are not supported by Odoo's built-in update mechanism. Some field types have changed (e.g. plain text → JSON), and Odoo cannot automatically migrate the data.

### Solution
Start fresh with a clean database for the new version:
```bash
make fclean
make up
make init
```

> ⚠️ This will permanently delete all existing data.
