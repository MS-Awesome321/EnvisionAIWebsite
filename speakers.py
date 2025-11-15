class SpeakerProfile():
  def __init__(self, name, organization, bio, img, link="", short_org="", active=False):
    self.name = name
    self.organization = organization
    self.short_org = short_org
    self.bio = bio
    self.img = img
    self.link = link
    self.active = active

class Speakers():
  def __init__(self, speakers):
    self.inactive = []
    self.active = []
    for speaker in reversed(speakers):
      if speaker.active:
        self.active.append(speaker)
      else:
        self.inactive.append(speaker)



SpeakerProfiles = [
  SpeakerProfile(
    "Cecilia Kang",
    "Technology and Regulatory Policy Reporter, New York Times",
    "Cecilia Kang is a technology reporter at The New York Times, where she covers the intersection of technology, policy, and politics, including AI regulation, antitrust efforts, and U.S.-China tech relations. She coauthored the acclaimed book An Ugly Truth: Inside Facebook’s Battle for Domination and has received George Polk and Loeb awards for her work.",
    "assets/speakers/kang.jpg",
    link="https://www.nytimes.com/by/cecilia-kang",
    short_org="Technology & Policy Reporter, New York Times"
  ),

  SpeakerProfile(
      "Patrick Achi",
      "Prime Minister, Côte d'Ivoire",
      "Patrick Achi is the Former Prime Minister of the Republic of Côte d’Ivoire. Patrick Achi was appointed Prime Minister, Chief of Government, from March 2021 to October 2023. From January 2017 to March 2021, he was Secretary General of the Presidency and Executive Secretary of the National Council for Economic Policy, in charge of preparing the Vision 2030 Strategic Development Plan of the country, with key emphasis on growth, food security, youth employment, human resources, and environment. During the preceding 17 years, from 2000 to 2017, he was Minister of Economic Infrastructure in charge of roads, water infrastructures, ports, airports, and railways development. He developed close ties with key DFI’s and implemented major PPP projects.",
      "assets/speakers/achi.jpg",
      link ="https://en.wikipedia.org/wiki/Patrick_Achi",
      short_org="Former Prime Minister of Côte d'Ivoire"
  ),

  SpeakerProfile(
      "Franklin Keller",
      "Founder and Chief Investment Officer, Talos Asset Management",
      "Franklin Keller is the Founder and Chief Investment Officer of Talos Asset Management, a Technology-focused hedge fund. Prior to founding Talos, he was Investment Director for the CHIPS Program Office (CPO) within the Department of Commerce – a $53bn grant and $75bn loan authority created by the bipartisan CHIPS Act of 2022 to bring semiconductor manufacturing back to America. Before joining the CPO, Mr. Keller was Associate Portfolio Manager at Ashler Capital (a Citadel business) focused on technology, a role he served from 2019-23. He was the Semiconductor Sector Head at Millennium Management from 2016-18 and started his investing career as an analyst at Balyasny Asset Management, where he worked from 2014-16. Prior to joining the buyside, he worked in sell-side equity research at Morgan Stanley from 2013-14 and Lehman Brothers / Barclays from 2008-13, covering semiconductors.",
      "assets/speakers/keller.jpg",
      link = "https://jrc.princeton.edu/SpeakerProfiles/franklin-keller",
      short_org="Founder and CIO, Talos Asset Management"
  ),

  SpeakerProfile(
    "Happy Buzaaba",
    "Postdoctoral Research Associate in African Language Technologies, Princeton's Center for Digital Humanities",
    "Happy Buzaaba is a Postdoctoral Research Associate at Princeton University's Center for Digital Humanities, focusing on developing technologies for low-resource African languages.He earned his Ph.D. in Systems and Information Engineering from the University of Tsukuba, where he specialized in machine learning and computational linguistics.",
    "assets/speakers/buzaaba.jpg",
    link ="https://buzaabah.github.io/",
    short_org="Princeton Researcher in African Language Technologies"
  ),

  

  SpeakerProfile(
    "Josua New",
    "Director of Policy, SeedAI",
    "Joshua New is the Director of Policy for SeedAI, responsible for SeedAI’s public policy thought leadership. Previously, Joshua led the public policy portfolio for generative AI and AI safety, open innovation, and other technology and science policy issues at IBM. At IBM, Joshua helped launch the AI Alliance, an international community focused on developing AI collaboratively, transparently, and with a focus on safety, ethics, and the greater good, and served as co-chair of the AI Alliance’s policy working group. Prior to IBM, Joshua was a Senior Policy Analyst at the Information Technology and Innovation Foundation’s (ITIF) Center for Data Innovation, where he focused on AI, emerging data-driven technologies, and open innovation.",
    "assets/speakers/new.jpg",
    link="https://www.linkedin.com/in/joshua-new-00b28758/",
    short_org="Director of Policy, SeedAI"
  ),

  SpeakerProfile(
    "Luke Chan",
    "Chief of Staff at Cofactor",
    "Luke Chan is the Chief of Staff at Cofactor, which builds AI to be healthcare's first true financial intelligence layer. They help providers tackle their most complex denials so that they can focus on what really matters.",
    "assets/speakers/chan.jpeg",
    link="https://www.linkedin.com/in/lukemchan/",
    short_org="Chief of Staff, Cofactor"
  ),

  SpeakerProfile(
    "Gabriel Daly",
    "Associate General Counsel, US Department of Energy",
    "Gabriel Daly is a legal advisor and Associate General Counsel at the United States Department of Energy. His speciality lies at the intersection of law, energy systems, and power-hungry AI, where he focuses on the challenge of supplying modern AI technologies with the resources they need to function while making these systems more energy efficient overall.",
    "assets/speakers/daly.png",
    link="https://www.linkedin.com/in/gabriel-daly-0527b423/",
    short_org="Associate General Counsel, US Department of Energy"
  ),

  SpeakerProfile(
      "Akash Kapur",
      "Senior Fellow, The GovLab at NYU, Princeton Visiting Research Professor",
      "Akash Kapur is an academic and writer specializing in data policy, Internet governance, digital public infrastructure, and digital inclusion. He is a senior fellow at The GovLab at NYU and a founding member of the Academic Advisory Council for Krea University in Chennai. Kapur has consulted for organizations including UNDP and the Markle Foundation, bringing expertise in technology policy and governance. A former columnist for The New York Times, he contributes regularly to The New Yorker, The Wall Street Journal, and The Economist. He is the author of Better to Have Gone and India Becoming, both named New York Times Editor’s Choices. Kapur holds a B.A. in Social Anthropology from Harvard and a D.Phil. in Law from Oxford, where he was a Rhodes Scholar.",
      "assets/speakers/kapur.jpg",
      link="https://cgi.princeton.edu/people/akash-kapur",
      short_org="Senior Fellow at The GovLab at NYU, Princeton Visiting Research Professor"
    ),
    SpeakerProfile(
      "Vikram V. Ramaswamy",
      "Lecturer, Princeton University",
      "Vikram V. Ramaswamy is a teaching faculty member in Princeton University’s Computer Science Department, where he teaches introductory courses in artificial intelligence and machine learning. His work focuses on fairness and interpretability in machine learning, with an emphasis on visual systems. Ramaswamy has developed improved real and synthetic datasets and produced influential analyses of interpretability methods for convolutional neural networks. He received his Ph.D. from Princeton University under the supervision of Prof. Olga Russakovsky, and earned his bachelor’s and master’s degrees from IIT Madras, where he was advised by Prof. Jayalal Sarma.",
      "assets/speakers/vikram.jpg",
      link="https://www.cs.princeton.edu/~vr23/",
      short_org="Lecturer, Princeton University",
      active=True
    ),
    SpeakerProfile(
      "Steven Kelts",
      "Lecturer, Princeton University",
      "Steven Kelts is a Lecturer in Princeton University’s School of Public and International Affairs and Department of Computer Science. His work centers on ethics in technology, including the distinctive moral responsibilities of modern tech firms, with peer-reviewed publications in Technology and Society Magazine and the IEEE International Symposium on Technology and Society. Kelts is an ethics advisor to the Responsible A.I. Institute and the recipient of grants from Princeton’s Council on Science and Technology and from Google for the “Agile Ethics” program. He leads Princeton’s GradFutures initiative on the Ethics of AI, for which he earned the university’s Clio Hall Award. Beyond his teaching and scholarship, Kelts co-founded Kalos Academy, a nonprofit supporting first-generation and low-income students, and has contributed curriculum design for Tsinghua University and the EdTech platform Campus.org.",
      "assets/speakers/kelts.jpeg",
      link="https://www.stevenkelts.com/",
      short_org="Lecturer, Princeton University",
      active=True
    ),
    SpeakerProfile(
    "Noah Broestl",
    "Partner and Associate Director, Responsible AI, BCG",
    "Noah Broestl is a Partner and Associate Director of Responsible AI at Boston Consulting Group (BCG), focusing on implementing ethical AI frameworks across various industries. Prior to joining BCG, he spent 13 years at Google, contributing to projects in vendor management, infrastructure engineering, abuse response, and artificial intelligence. Academically, Noah holds a Master's in Practical Ethics from the University of Oxford, where he explored topics including climate ethics. He is also a member of the Green Software Foundation's Steering Committee, contributing to sustainable software development practices.",
    "assets/speakers/broestl.jpg",
    link="https://github.com/orgs/Green-Software-Foundation/discussions/135",
    short_org="BCG Responsible AI Associate Director",
    active=True
  ),
    SpeakerProfile(
      "Arvind Narayanan",
      "Professor, Princeton University",
      "Arvind Narayanan is a Professor of Computer Science at Princeton University and Director of the Center for Information Technology Policy. He is the co-author of AI Snake Oil—both the book and its widely read newsletter, followed by over 50,000 researchers, policymakers, journalists, and AI enthusiasts—and previously co-authored the influential textbooks Bitcoin and Cryptocurrency Technologies and Fairness in Machine Learning. Narayanan led the Princeton Web Transparency and Accountability Project, producing landmark work on data practices and demonstrating some of the earliest evidence that machine learning systems echo cultural biases. Named to TIME’s inaugural list of the 100 most influential people in AI, he has also received the Presidential Early Career Award for Scientists and Engineers (PECASE).",
      "assets/speakers/arvind.jpg",
      link="https://www.cs.princeton.edu/~arvindn/",
      short_org="Professor, Princeton University",
      active=True
    ),
    
    

]

speakers = Speakers(SpeakerProfiles)