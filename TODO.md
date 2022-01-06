# ASA->FDM object parser
Python script for configuring objects and object-groups taken from a running ASA and parse them to a Firepower running standalone, FDM.

### ToDo
- [ ] Report to user wheter the migration was a success
- [ ] Migrate NAT rules

### In progess
- Handle deployment status
- Migrate access-lists

### Completed Tasks ✓
- [x] Handle service/port objects
- [x] If a network group contains an IP host/subnet, it must be converted to an object before its assigned to the group.
- [x] Get token from ASA
- [x] Get token from FDM
- [x] Get network objects from ASA
- [x] Get network object-groups from ASA
- [x] Parse network objects from to FDM
- [x] Parse network object-groups to FDM
- [x] Delete every non-system-defined object on FDM
- [x] Handle HTTP error codes 
  - [x] Handle HTTP error code 422, duplicate entry
  - [x] Handle HTTP error code 'unauthorized'    
