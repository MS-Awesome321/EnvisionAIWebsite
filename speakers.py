class Speaker():
  def __init__(self, name, organization, bio, img):
    self.name = name
    self.organization = organization
    self.bio = bio 
    self.img = img


speakers = [
  Speaker(
    "Emmett Souder",
    "Envision Princeton",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer luctus volutpat maximus. Fusce iaculis commodo turpis, quis feugiat arcu dapibus sit amet. Morbi nec nisi suscipit, lobortis massa sed, volutpat tellus. Nullam ultrices suscipit urna, id ultricies ex aliquam sit amet. Sed porta imperdiet felis vitae mattis. Ut non mauris libero. Fusce id feugiat risus. Fusce aliquam nulla sit amet nulla sodales, ut congue sapien tincidunt. Nulla lobortis velit in egestas ultricies. Fusce auctor diam placerat quam tincidunt, vitae bibendum sapien dapibus. Nunc at orci quis metus lacinia pulvinar at in metus. Suspendisse non risus at felis tristique blandit et non sem. Maecenas accumsan dui ut ex dapibus, ac faucibus enim tristique. Donec eget hendrerit ligula, ut interdum elit. Curabitur vestibulum, neque convallis mattis efficitur, ex nunc tincidunt nunc, sit amet accumsan leo leo at ipsum.",
    "assets/team/emmett.jpg",
  ),

  Speaker(
    "Maddie Feldman",
    "Envision Princeton",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer luctus volutpat maximus. Fusce iaculis commodo turpis, quis feugiat arcu dapibus sit amet. Morbi nec nisi suscipit, lobortis massa sed, volutpat tellus. Nullam ultrices suscipit urna, id ultricies ex aliquam sit amet. Sed porta imperdiet felis vitae mattis. Ut non mauris libero. Fusce id feugiat risus. Fusce aliquam nulla sit amet nulla sodales, ut congue sapien tincidunt. Nulla lobortis velit in egestas ultricies. Fusce auctor diam placerat quam tincidunt, vitae bibendum sapien dapibus. Nunc at orci quis metus lacinia pulvinar at in metus. Suspendisse non risus at felis tristique blandit et non sem. Maecenas accumsan dui ut ex dapibus, ac faucibus enim tristique. Donec eget hendrerit ligula, ut interdum elit. Curabitur vestibulum, neque convallis mattis efficitur, ex nunc tincidunt nunc, sit amet accumsan leo leo at ipsum.",
    "assets/team/maddie.jpg",
  ),
]