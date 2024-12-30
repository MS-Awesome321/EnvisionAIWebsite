class Speaker():
  def __init__(self, name, organization, bio, img, link=""):
    self.name = name
    self.organization = organization
    self.bio = bio 
    self.img = img
    self.link = link

speakers = [
  Speaker(
    "Cecelia Kang",
    "Technology and Regulatory Policy Reporter, New York Times",
    "Cecilia Kang is a technology reporter at The New York Times, where she covers the intersection of technology, policy, and politics, including AI regulation, antitrust efforts, and U.S.-China tech relations. She coauthored the acclaimed book An Ugly Truth: Inside Facebook’s Battle for Domination and has received George Polk and Loeb awards for her work.",
    "assets/speakers/kang.jpg",
    "https://www.nytimes.com/by/cecilia-kang"
  ),

  Speaker(
    "Liz Stotland Weiswasser",
    "Co-Chair, Litigation Department, Paul, Weiss, Rifkind, Wharton & Garrison LLP",
    "Liz Stotland Weiswasser is a nationally renowned litigator and counselor specializing in life sciences and technology, now co-chair of the Litigation Department at Paul, Weiss. With accolades such as 'IP Litigator of the Year' and a career spanning patent litigation, biopharma technologies, and high-stakes competitor disputes, she brings unparalleled expertise to the intersection of innovation and regulatory challenges.",
    "assets/speakers/weiswasser.jpeg",
    "https://www.paulweiss.com/professionals/partners-and-counsel/elizabeth-stotland-weiswasser"
  ),

  Speaker(
    "Christian Chung",
    "International Security and Emerging Technologies Advisor, PhD Student, Princeton SPIA",
    "Christian Chung is a Ph.D. student at Princeton University’s School of Public and International Affairs, researching the impact of advanced AI on military strategy, strategic stability, and deterrence. With over a decade of experience as a U.S. Government foreign affairs analyst and his current role as a U.S. Navy Reserve Intelligence Officer, he brings a wealth of expertise in international security and emerging technologies to the discussion.",
    "assets/speakers/chung.jpg",
    "https://www.iaps.ai/christian-chung"
  ),

  Speaker(
    "Katherine Lee",
    "Staff Research Scientist, Google DeepMind",
    "Katherine Lee is a senior research scientist at Google DeepMind and director of the GenLaw Center, where she studies the intersection of generative AI, security, privacy, and legal implications. With expertise in data extraction, AI model alignment, and copyright concerns, she has led workshops like GenLaw ’23 at ICML and published groundbreaking research recognized at ACL, USENIX, and ICLR.",
    "assets/speakers/lee.jpg",
    "https://katelee168.github.io/"
  ),

  Speaker(
    "Noah Broestl",
    "Partner and Associate Director, Responsible AI, BCG",
    "Noah Broestl is a Partner and Associate Director of Responsible AI at Boston Consulting Group (BCG), focusing on implementing ethical AI frameworks across various industries. Prior to joining BCG, he spent 13 years at Google, contributing to projects in vendor management, infrastructure engineering, abuse response, and artificial intelligence. Academically, Noah holds a Master's in Practical Ethics from the University of Oxford, where he explored topics including climate ethics. He is also a member of the Green Software Foundation's Steering Committee, contributing to sustainable software development practices.",
    "assets/speakers/broestl.jpeg",
    "https://github.com/orgs/Green-Software-Foundation/discussions/135?utm_source=chatgpt.com"
  ),

  Speaker(
    "Happy Buzaaba",
    "Postdoctoral Research Associate in African Language Technologies, Princeton's Center for Digital Humanities",
    "Happy Buzaaba is a Postdoctoral Research Associate at Princeton University's Center for Digital Humanities, focusing on developing technologies for low-resource African languages.He earned his Ph.D. in Systems and Information Engineering from the University of Tsukuba, where he specialized in machine learning and computational linguistics.",
    "assets/speakers/buzaaba.jpg",
    "https://buzaabah.github.io/"
  )
]