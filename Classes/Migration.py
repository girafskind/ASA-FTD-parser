# ASA-FTD object parser
# Migration.py - class file
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

# Migration class, keeps track on objects
class MigrationStatus:

    network_objects_in_asa = 0
    group_objects_in_asa = 0

    migrated_network_objects = 0
    migrated_group_objects = 0

    skipped_caused_by_duplicates = 0

    skipped_objects = []

    def add_net(self):
        self.network_objects_in_asa = self.network_objects_in_asa + 1

    def add_group(self):
        self.group_objects_in_asa = self.group_objects_in_asa + 1

    def add_migrated_net(self):
        self.migrated_network_objects = self.migrated_network_objects + 1

    def add_migrated_group(self):
        self.migrated_group_objects = self.migrated_group_objects + 1

    def add_duplicate(self):
        self.skipped_caused_by_duplicates = self.skipped_caused_by_duplicates + 1
