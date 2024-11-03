import argparse
import importlib
import os
import asyncio
from datetime import datetime
from app.dependencies import get_mongo_db
from faker import Faker

MIGRATIONS_DIR = "database/migrations"
SEEDS_DIR = "database/seeders"
fake = Faker()

async def initialize_versioning_table(db):
    if "migrations" not in (await db.list_collection_names()):
        await db.create_collection("migrations")
        print("Created 'migrations' collection for versioning.")

def list_migrations():
    files = os.listdir(MIGRATIONS_DIR)
    migrations = [f.split(".")[0] for f in files if f.startswith("migration_")]
    migrations.sort()
    return migrations

def create_migration(name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"migration_{timestamp}_{name}.py"
    path = os.path.join(MIGRATIONS_DIR, filename)
    with open(path, "w") as f:
        f.write(
            "def upgrade(db):\n"
            "    # TODO: Write upgrade logic here\n"
            "    pass\n\n"
            "def downgrade(db):\n"
            "    # TODO: Write downgrade logic here\n"
            "    pass\n"
        )
    print(f"Created migration: {filename}")

async def upgrade_migrations(run_seed=False):
    db = get_mongo_db()
    if db is None:
        raise RuntimeError("Database connection failed. Cannot proceed with migrations.")

    await initialize_versioning_table(db)

    applied_migrations = await get_applied_migrations(db)
    migrations = list_migrations()

    for migration_name in migrations:
        if migration_name not in applied_migrations:
            print(f"Applying migration: {migration_name}")
            migration_module = importlib.import_module(f"database.migrations.{migration_name}")
            migration_module.upgrade(db)
            await db["migrations"].insert_one({"version": migration_name})
            print(f"Migration {migration_name} applied.")
        else:
            print(f"Migration {migration_name} already applied.")

    if run_seed:
        await run_all_seeds()

async def downgrade_migrations(all=False):
    db = get_mongo_db()
    if db is None:
        print("Database connection failed.")
        return

    applied_migrations = await get_applied_migrations(db)
    migrations = list_migrations()
    migrations.reverse()

    if all:
        for migration_name in migrations:
            if migration_name in applied_migrations:
                print(f"Reverting migration: {migration_name}")
                migration_module = importlib.import_module(f"database.migrations.{migration_name}")
                migration_module.downgrade(db)
                await db["migrations"].delete_one({"version": migration_name})
                print(f"Migration {migration_name} reverted.")
        print("All migrations have been reverted.")
    else:
        for migration_name in migrations:
            if migration_name in applied_migrations:
                print(f"Reverting migration: {migration_name}")
                migration_module = importlib.import_module(f"database.migrations.{migration_name}")
                migration_module.downgrade(db)
                await db["migrations"].delete_one({"version": migration_name})
                print(f"Migration {migration_name} reverted.")
                break
        else:
            print("No migrations to revert.")

async def get_applied_migrations(db):
    applied_migrations = await db["migrations"].find().to_list(length=None)
    return {m["version"] for m in applied_migrations}

# Create a new seed file
def create_seed(name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"seed_{timestamp}_{name}.py"
    path = os.path.join(SEEDS_DIR, filename)
    with open(path, "w") as f:
        f.write(
            "from faker import Faker\n"
            "from core.database import get_mongo_db\n\n"
            "fake = Faker()\n\n"
            "async def seed(db):\n"
            "    # TODO: Add seed logic here\n"
            "    data = []\n"
            "    for _ in range(10):\n"
            "        data.append({\n"
            "            'name': fake.name(),\n"
            "            'email': fake.email(),\n"
            "            'created_at': fake.date_time_this_decade()\n"
            "        })\n"
            "    await db['your_collection'].insert_many(data)\n"
            "    print('Seeded your_collection')\n"
        )
    print(f"Created seed: {filename}")

async def run_seed(seed_name):
    db = get_mongo_db()
    if db is None:
        print("Database connection failed.")
        return

    seed_file = f"seed_{seed_name}.py"
    print(f"Loading specific seed file: {seed_file}")
    seed_module = importlib.import_module(f"database.seeders.{seed_name}")
    seed_func = getattr(seed_module, "seed", None)

    if seed_func is not None and callable(seed_func):
        await seed_func(db)
        print(f"Executed seed: {seed_file}")
    else:
        print(f"No callable 'seed' function found in {seed_file}")

async def run_all_seeds():
    db = get_mongo_db()
    if db is None:
        print("Database connection failed.")
        return

    seed_files = [f.split(".")[0] for f in os.listdir(SEEDS_DIR) if f.endswith(".py")]
    print("Found seed files:", seed_files)

    for seed_file in seed_files:
        print(f"Loading seed file: {seed_file}")
        seed_module = importlib.import_module(f"database.seeders.{seed_file}")
        seed_func = getattr(seed_module, "seed", None)

        if seed_func is not None and callable(seed_func):
            print(f"Running seed function in {seed_file}")
            await seed_func(db)
            print(f"Executed seed: {seed_file}")
        else:
            print(f"No callable 'seed' function found in {seed_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database migration and seeding runner")
    parser.add_argument("command", help="Command to run (migrate:create, migrate:upgrade, migrate:down, migrate, seed:run, seed:create)")
    parser.add_argument("--name", help="Name for the new migration or seed (required for migrate:create and seed:create commands)")
    parser.add_argument("--all", action="store_true", help="Revert all migrations (only for migrate:down command)")
    parser.add_argument("--seed", action="store_true", help="Run all seeds after migrations (only for migrate:up command)")

    args = parser.parse_args()

    if args.command == "migrate:create":
        if not args.name:
            print("Error: --name is required for migrate:create command")
        else:
            create_migration(args.name)
    # elif args.command == "migrate:up":
    #     asyncio.run(upgrade_migrations(run_seed=args.seed))
    elif args.command == "migrate:down":
        if args.all:
            asyncio.run(downgrade_migrations(all=True))
        else:
            asyncio.run(downgrade_migrations())
    elif args.command == "migrate:run":
        # asyncio.run(upgrade_migrations())
        if args.seed:
            asyncio.run(upgrade_migrations(run_seed=True))
        else:
            asyncio.run(upgrade_migrations())
    elif args.command == "seed:run":
        if args.seed:
            asyncio.run(run_seed(args.seed))
        else:
            asyncio.run(run_all_seeds())
    elif args.command == "seed:create":
        if not args.name:
            print("Error: --name is required for seed:create command")
        else:
            create_seed(args.name)
    else:
        print(f"Unknown command: {args.command}")
