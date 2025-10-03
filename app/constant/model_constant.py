MEMBER_ROLE = 'member'
MANAGER_ROLE = 'manager'

ROLE_CHOICES = [
    (MEMBER_ROLE, 'Event Member'),
    (MANAGER_ROLE, 'Event Manager')
]

# Status event
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

REGISTERED_ATTENDEE = 'registered'
CONFIRMED_ATTENDEE = 'confirmed'
CANCELLED_ATTENDEE = 'cancelled'

ATTENDEE_STATUS = [
    (REGISTERED_ATTENDEE, 'Registered'),
    (CONFIRMED_ATTENDEE, 'Confirmed'),
    (CANCELLED_ATTENDEE, 'Cancelled'),
]   

_g = globals().copy() 
CONSTANT_LIST = {
    name: value
    for name, value in _g.items()
    if isinstance(value, str)
}
