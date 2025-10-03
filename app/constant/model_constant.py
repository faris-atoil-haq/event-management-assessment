MEMBER_ROLE = 'member'
MANAGER_ROLE = 'manager'
    
_g = globals().copy() 
CONSTANT_LIST = {
    name: value
    for name, value in _g.items()
    if isinstance(value, str)
}
