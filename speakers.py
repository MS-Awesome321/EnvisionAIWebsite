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
      "Patrick Achi",
      "Prime Minister, Côte d'Ivoire",
      "Patrick Achi is the Former Prime Minister of the Republic of Côte d’Ivoire. Patrick Achi was appointed Prime Minister, Chief of Government, from March 2021 to October 2023. From January 2017 to March 2021, he was Secretary General of the Presidency and Executive Secretary of the National Council for Economic Policy, in charge of preparing the Vision 2030 Strategic Development Plan of the country, with key emphasis on growth, food security, youth employment, human resources, and environment. During the preceding 17 years, from 2000 to 2017, he was Minister of Economic Infrastructure in charge of roads, water infrastructures, ports, airports, and railways development. He developed close ties with key DFI’s and implemented major PPP projects.",
      "assets/speakers/achi.jpg",
      "https://en.wikipedia.org/wiki/Patrick_Achi"
  ),

  Speaker(
    "Liz Stotland Weiswasser",
    "Co-Chair, Litigation Department, Paul, Weiss, Rifkind, Wharton & Garrison LLP",
    "Liz Stotland Weiswasser is a nationally renowned litigator and counselor specializing in life sciences and technology, now co-chair of the Litigation Department at Paul, Weiss. With accolades such as 'IP Litigator of the Year' and a career spanning patent litigation, biopharma technologies, and high-stakes competitor disputes, she brings unparalleled expertise to the intersection of innovation and regulatory challenges.",
    "assets/speakers/weiswasser.jpeg",
    "https://www.paulweiss.com/professionals/partners-and-counsel/elizabeth-stotland-weiswasser"
  ),

  Speaker(
      "Franklin Keller",
      "Founder and Chief Investment Officer, Talos Asset Management",
      "Franklin Keller is the Founder and Chief Investment Officer of Talos Asset Management, a Technology-focused hedge fund. Prior to founding Talos, he was Investment Director for the CHIPS Program Office (CPO) within the Department of Commerce – a $53bn grant and $75bn loan authority created by the bipartisan CHIPS Act of 2022 to bring semiconductor manufacturing back to America. Before joining the CPO, Mr. Keller was Associate Portfolio Manager at Ashler Capital (a Citadel business) focused on technology, a role he served from 2019-23. He was the Semiconductor Sector Head at Millennium Management from 2016-18 and started his investing career as an analyst at Balyasny Asset Management, where he worked from 2014-16. Prior to joining the buyside, he worked in sell-side equity research at Morgan Stanley from 2013-14 and Lehman Brothers / Barclays from 2008-13, covering semiconductors.",
      "assets/speakers/keller.jpg",
      "https://jrc.princeton.edu/speakers/franklin-keller"
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
    "Happy Buzaaba",
    "Postdoctoral Research Associate in African Language Technologies, Princeton's Center for Digital Humanities",
    "Happy Buzaaba is a Postdoctoral Research Associate at Princeton University's Center for Digital Humanities, focusing on developing technologies for low-resource African languages.He earned his Ph.D. in Systems and Information Engineering from the University of Tsukuba, where he specialized in machine learning and computational linguistics.",
    "assets/speakers/buzaaba.jpg",
    "https://buzaabah.github.io/"
  ),

  Speaker(
    "Noah Broestl",
    "Partner and Associate Director, Responsible AI, BCG",
    "Noah Broestl is a Partner and Associate Director of Responsible AI at Boston Consulting Group (BCG), focusing on implementing ethical AI frameworks across various industries. Prior to joining BCG, he spent 13 years at Google, contributing to projects in vendor management, infrastructure engineering, abuse response, and artificial intelligence. Academically, Noah holds a Master's in Practical Ethics from the University of Oxford, where he explored topics including climate ethics. He is also a member of the Green Software Foundation's Steering Committee, contributing to sustainable software development practices.",
    "assets/speakers/broestl.jpg",
    "https://github.com/orgs/Green-Software-Foundation/discussions/135"
  ),

  Speaker(
    "Josua New",
    "Director of Policy, SeedAI",
    "Joshua New is the Director of Policy for SeedAI, responsible for SeedAI’s public policy thought leadership. Previously, Joshua led the public policy portfolio for generative AI and AI safety, open innovation, and other technology and science policy issues at IBM. At IBM, Joshua helped launch the AI Alliance, an international community focused on developing AI collaboratively, transparently, and with a focus on safety, ethics, and the greater good, and served as co-chair of the AI Alliance’s policy working group. Prior to IBM, Joshua was a Senior Policy Analyst at the Information Technology and Innovation Foundation’s (ITIF) Center for Data Innovation, where he focused on AI, emerging data-driven technologies, and open innovation.",
    "assets/speakers/new.jpg",
    ""
  ),

  Speaker(
    "Luke Chan",
    "Chief of Staff at Cofactor",
    "Luke Chan is the Chief of Staff at Cofactor, which builds AI to be healthcare's first true financial intelligence layer. They help providers tackle their most complex denials so that they can focus on what really matters."
    "assets/speakers/chan.jpeg",
    "https://www.linkedin.com/in/lukemchan/"
  ),

  Speaker(
    "Gabriel Daly",
    "Associate General Counsel, US Department of Energy",
    "Gabriel Daly is a legal advisor and Associate General Counsel at the United States Department of Energy. His speciality lies at the intersection of law, energy systems, and power-hungry AI, where he focuses on the challenge of supplying modern AI technologies with the resources they need to function while making these systems more energy efficient overall.",
    "assets/speakers/daly.png",
    "https://www.linkedin.com/in/gabriel-daly-0527b423/"
  ),
]