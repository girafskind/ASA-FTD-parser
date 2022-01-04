# ASA-FTD object parser
# Migration.py - class file
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

# Migration class, keeps track on objects
class MigrationStatus:

    network_objects_in_asa = 0
    network_object_groups_in_asa = 0
    service_objects_in_asa = 0
    service_object_groups_in_asa = 0

    migrated_network_objects = 0
    migrated_network_object_groups = 0
    migrated_service_objects = 0
    migrated_service_object_groups = 0

    skipped_nets_caused_by_duplicates = 0
    skipped_services_caused_by_duplicates = 0
    skipped_service_groups_caused_by_duplicates = 0

    skipped_objects = []

    def add_net(self):
        self.network_objects_in_asa = self.network_objects_in_asa + 1

    def add_group(self):
        self.network_object_groups_in_asa = self.network_object_groups_in_asa + 1

    def add_migrated_net(self):
        self.migrated_network_objects = self.migrated_network_objects + 1

    def add_migrated_group(self):
        self.migrated_network_object_groups = self.migrated_network_object_groups + 1

    def add_migrated_service(self):
        self.migrated_service_objects = self.migrated_service_objects + 1

    def add_migrated_service_group(self):
        self.migrated_service_object_groups = self.migrated_service_object_groups + 1

    def add_duplicate_network(self, duplicate_network, reason):
        self.skipped_nets_caused_by_duplicates = self.skipped_nets_caused_by_duplicates + 1
        self.skipped_objects.append({'skipped item': duplicate_network, 'type': 'service object', 'reason': reason})

    def add_duplicate_service(self, duplicate_service, reason):
        self.skipped_services_caused_by_duplicates = self.skipped_services_caused_by_duplicates + 1
        self.skipped_objects.append({'skipped item': duplicate_service, 'type': 'service object', 'reason': reason})

    def add_duplicate_service_group(self, duplicate_service_group, reason):
        self.skipped_service_groups_caused_by_duplicates = self.skipped_service_groups_caused_by_duplicates + 1
        self.skipped_objects.append({'skipped item': duplicate_service_group, 'type': 'service object', 'reason': reason})

    def skipped_objects_in_migration(self):
        return self.skipped_nets_caused_by_duplicates + self.skipped_services_caused_by_duplicates
