from migrate_exe import importer_migrate, model_migrate


if __name__ == "__main__":
    model_migrate.run_migrate('gpt-4o-mini')
    #importer.run_importer()