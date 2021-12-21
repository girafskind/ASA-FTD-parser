# ASA->FDM object parser
Python script for configuring objects and object-groups taken from a running ASA and parse them to a Firepower running standalone, FDM.

### ToDo
- [ ] Handle HTTP error codes 
  - [ ] Handle HTTP error code 422, duplicate entry
  - [ ] Handle HTTP error code 'unauthorized'    
- [ ] Handle service/port objects
- [ ] Report to user wheter the migration was a success
- [ ] If a network group contains an IP host/subnet, it must be converted to an object before its assigned to the group. 

### In progess
- Handle deployment status

### Completed Tasks ✓
- [x] Get token from ASA
- [x] Get token from FDM
- [x] Get network objects from ASA
- [x] Get network object-groups from ASA
- [x] Parse network objects from to FDM
- [x] Parse network object-groups to FDM
- [x] Delete every non-system-defined object on FDM