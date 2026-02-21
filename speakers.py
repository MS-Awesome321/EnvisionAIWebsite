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
    "Noah Broestl",
    "Partner and Associate Director, Responsible AI, BCG",
    "Noah Broestl is a Partner and Associate Director of Responsible AI at Boston Consulting Group (BCG), focusing on implementing ethical AI frameworks across various industries. Prior to joining BCG, he spent 13 years at Google, contributing to projects in vendor management, infrastructure engineering, abuse response, and artificial intelligence. Academically, Noah holds a Master's in Practical Ethics from the University of Oxford, where he explored topics including climate ethics. He is also a member of the Green Software Foundation's Steering Committee, contributing to sustainable software development practices.",
    "assets/speakers/broestl.jpg",
    link="https://github.com/orgs/Green-Software-Foundation/discussions/135",
    short_org="BCG Responsible AI Associate Director",
    active=True
  ),
  SpeakerProfile(
      "Michelle Ma",
      "Organizer, Network on Emerging Threats",
      "Michelle Ma is an Organizer at the Network on Emerging Threats, a DC-based policy network connecting professionals focused on AI and biosecurity existential risk. She is an incoming Horizon Fellow and was previously a Research Manager at UChicago's Existential Risk Laboratory, researching federal regulatory precedents for emerging technologies. Michelle writes about AI progress and governance on Substack, has written for Works in Progress, and was an AI Blogging Fellow at Asterisk Magazine. She holds a B.A. in Economics from the University of Chicago.",
      "assets/speakers/parent.jpg",
      link="https://www.linkedin.com/in/michelle-ma-99837227b/",
      short_org="Organizer, Network on Emerging Threats",
      active=True
    ),
    SpeakerProfile(
      "Jesse Parent",
      "Senior Program Manager, Data x Direction (DxD)",
      "Jesse Parent is a strategist and data scientist helping visionary teams and aspiring philosopher-builders map the path from here to there. He works at the intersection of foresight, research architecture, and mentorship, turning complexity into clear on-ramps for action. He is Senior Program Manager at Data x Direction, a project and learning platform exploring data science, data ethics, human-centered AI, and strategic decision-making through educational materials, discussion series, content, and internships focused on responsible AI, practical data strategy, and the human and systems-level impacts of data-driven choices. He also directs JOPRO, supporting interdisciplinary inquiry and future-oriented leadership through talks, workshops, and community-based learning.",
      "assets/speakers/parent.jpg",
      link="https://jesparent.com/",
      short_org="Senior Program Manager, Data x Direction (DxD)",
      active=True
    ),
    SpeakerProfile(
      "MSA AI Team",
      "Amber Berry, Vice President of AI; Morgan Mifflin, AI Project Manager",
      "Middle States Association (MSA) is a global accrediting organization that launched the RAIL: Responsible AI in Learning endorsement series to provide the only implementation framework of its kind to support schools in wise change. MSA’s AI Team guides school leaders to move beyond tools to human-led, ethical, and mission-aligned systems. Amber Berry ‘08 is the Vice President of AI & Strategy and co-founder of RAIL. She brings 15 years of school experience as a former teacher and principal with deep expertise in school transformation, adult learning, and ethical AI adoption at scale. Amber is an alumna of Princeton, holds a Master’s from Middlebury, and a Master’s of Education from Columbia, and a Mini-MBA from SectionAI.\n Morgan Mifflin is an AI Project Manager at MSA. She supports Evolution Lab initiatives that guide schools through their AI transformation journeys. Morgan holds a Master of Arts in International Security with a specialization in cybersecurity and AI ethics.",
      "assets/speakers/berry-mifflin1.png",
      link="https://www.msaevolutionlab.com/rail",
      short_org="MSA Responsible AI in Learning Team",
      active=True
    ),
    SpeakerProfile(
      "Benedikt Lehnert",
      "Entrepreneurship & Design Fellow, Princeton University; CEO of 74West",
      "Benedikt is the founder of 74West, a hands-on advisory practice for CEOs, executives, or boards who are navigating pivotal moments in their organizations. Benedikt also serves as an Entrepreneurship & Design Fellow at Princeton University, where he teaches aspiring entrepreneurs at the Keller Center. His work explores the convergence of entrepreneurship, humanistic design, and business leadership with a focus on AI and co-creativity, neuroaesthetics, and the socio-economic responsibility of design. As a board member of the Design Executive Council (DXC) Ben helps shape the standards of humanistic design and strategic leadership as AI transforms experience design and business strategy. Previously, he served as Chief Design Officer at Stark, led global design transformation at SAP, directed major UX teams at Microsoft, and served as Chief Design Officer at Wunderlist. Benedikt is also the author of Typoguide, an angel investor in design-driven startups, and an international keynote speaker whose award-winning work across hardware, software, and brand design has been featured worldwide.",
      "assets/speakers/lehnert.jpg",
      link="https://benediktlehnert.github.io/",
      short_org="CEO,74West; Fellow, Princeton University",
      active=True
    ),
    SpeakerProfile(
    "Alexander Kriebitz",
    "Political Scientist, Technical University of Munich",
    "Alexander Kriebitz is a political scientist at the Technical University of Munich whose work sits at the intersection of international law, business ethics, and international relations. His current research re-examines scholarship on Business and Human Rights, focusing on how responsibilities for upholding human rights are divided between states and companies. His work has published in the Business and Human Rights Journal, AI and Ethics, and Human Rights Review. He is a key collaborator on the AI & Human Rights project at the AI Ethics Lab at Rutgers University, a comprehensive legal framework that maps which rights AI can threaten or advance, how risks play out across sectors, and who is accountable for protecting them.",
    "assets/speakers/kriebitz.jpg",
    link="https://www.gov.sot.tum.de/en/wirtschaftsethik/team/kriebitz/",
    short_org="Political Scientist, Technical University of Munich",
    active=True
  ),
    SpeakerProfile(
    "Tammy Kwan",
    "Entrepreneur in Residence, Princeton University",
    "Tammy Kwan is an entrepreneur and researcher focused on the intersection of artificial intelligence, education, and human development. She currently serves as Vice President of Product at Teaching Strategies and Entrepreneur-in-Residence at Princeton University’s AI Lab. She writes and speaks on topics related to AI in education, child development, and the future of learning. Previously, she co-founded Cognitive ToyBox and led the company through its acquisition by Teaching Strategies in 2024. Cognitive ToyBox developed research-driven, game-based assessments for early childhood education. Her research and product work—supported by over $5M in funding—has helped shift district and state policy toward the use of developmentally appropriate direct assessment methods in early childhood classrooms, enabling more efficient and accurate measurement of children’s development in district and state-level early learning systems nationwide.",
    "assets/speakers/kwan.jpg",
    link="https://tammykwan.ai.princeton.edu/",
    short_org="Entrepreneur in Residence, Princeton University",
    active=True
  ),
    SpeakerProfile(
    "Nate Walker",
    "Founder, AI Ethics Lab at Rutgers University",
    "Dr. Nathan C. Walker is an award-winning First Amendment and human rights educator and founder of the AI Ethics Lab at Rutgers University. He has held research appointments at Harvard, Oxford, and Stellenbosch University in South Africa. The Rockefeller Foundation recently awarded him a Bellagio Residency to advance his research on AI ethics and human rights. Dr. Walker has worked with industry as an Expert AI Trainer for OpenAI and Handshake AI, provided ethics training to Adobe employees, and facilitated a working group at Google’s ethics-to-industry summit. He has published five books on law, education, and religion, and presented his research at the UN Human Rights Council, the Italian Ministry of Foreign Affairs, and the U.S. Senate. He earned his doctorate in First Amendment law and two master’s degrees from Columbia University. An ordained Unitarian Universalist minister, he holds a Master of Divinity from Union Theological Seminary.",
    "assets/speakers/walker.jpg",
    link="https://natewalker.com/",
    short_org="Founder, AI Ethics Lab at Rutgers",
    active=True
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
      "Edward You",
      "Former FBI Counterintelligence Leader; Founder & Principal, EHY Consulting",
      "Edward You is the Founder and Principal of EHY Consulting LLC, which focuses on the security, policy, and strategic implications of emerging technologies. He advises industry, academia, and government on the convergence of artificial intelligence, biotechnology, quantum, and other disruptive fields, helping organizations navigate the risks and opportunities shaping the future innovation landscape. He recently retired after more than two decades of service in the FBI, holding leadership roles at the intersection of counterintelligence, biosecurity, and technology protection. Most recently, he served on the FBI’s National Counterintelligence Task Force, advancing a whole-of-government approach to safeguarding emerging and disruptive technologies, and spent 15 years in the Weapons of Mass Destruction Directorate. He also completed a Joint Duty Assignment at the Office of the Director of National Intelligence as the National Counterintelligence Officer for Emerging and Disruptive Technologies.",
      "assets/speakers/you.jpg",
      link="https://www.linkedin.com/in/edward-you-1827bb1b/",
      short_org="Former FBI Counterintelligence; Founder, EHY Consulting",
      active=True
    ),
    SpeakerProfile(
      "Pallavi Nuka",
      "Associate Director, Julis-Rabinowitz Center for Public Policy & Finance; Lecturer, Princeton University",
      "Pallavi Nuka is Associate Director of Princeton SPIA’s Julis-Rabinowitz Center for Public Policy & Finance (JRCPPF). She helps lead the Center’s strategy and programs, oversees operations and academic initiatives, and works across campus with faculty, policymakers, alumni, and funders to advance multidisciplinary research, teaching, and student engagement on financial markets, macroeconomics, and economic policy. Previously, she was Associate Director of Princeton’s Innovations for Successful Societies program, where she researched governance and policy implementation and authored/edited publications on leadership and public-sector reform. She has also taught and conducted research at SPIA and Princeton Politics, and spent six years at the World Bank–GEF Evaluation Office evaluating climate and development investments in addition to serving in the U.S. Peace Corps in Côte d’Ivoire.",
      "assets/speakers/nuka.jpg",
      link="https://jrc.princeton.edu/people/pallavi-nuka",
      short_org="Associate Director of JRCPPF & Lecturer, Princeton University",
      active=True
    ),
    SpeakerProfile(
      "Jeffrey Oakman",
      "NJ AI Hub, Senior Strategic Project Manager",
      "Jeffrey Oakman  works with the Hub’s Executive Director in advancing the Hub’s goals of promoting advanced research in the field, driving regional economic growth and talent development in the tech sector, supporting private- and public-sector entities in AI utilization, and strengthening the AI start-up ecosystem in New Jersey. The NJ AI Hub is a first-of-its-kind public-private partnership between Princeton University, the New Jersey Economic Development Authority (NJEDA), Microsoft, and CoreWeave, designed to accelerate innovation in artificial intelligence and position New Jersey as a global leader in the field. Its aim is to bring together AI researchers, entrepreneurs, industry, educational institutions, and the public sector to advance world-class research and development; drive transformative AI innovation; empower the workforce for the AI era; and shape the future of responsible AI deployment.",
      "assets/speakers/oakman.png",
      link="https://njaihub.org/",
      short_org="NJ AI Hub Leadership Team",
      active=True
    ),
    SpeakerProfile(
      "Steven Kelts",
      "Lecturer, Princeton University; Ethics Advisor, Responsible A.I. Institute",
      "Steven Kelts is a Lecturer in Princeton University’s School of Public and International Affairs and Department of Computer Science. His work centers on ethics in technology, including the distinctive moral responsibilities of modern tech firms, with peer-reviewed publications in Technology and Society Magazine and the IEEE International Symposium on Technology and Society. Kelts is an ethics advisor to the Responsible A.I. Institute and the recipient of grants from Princeton’s Council on Science and Technology and from Google for the “Agile Ethics” program. He leads Princeton’s GradFutures initiative on the Ethics of AI, for which he earned the university’s Clio Hall Award. Beyond his teaching and scholarship, Kelts co-founded Kalos Academy, a nonprofit supporting first-generation and low-income students, and has contributed curriculum design for Tsinghua University and the EdTech platform Campus.org.",
      "assets/speakers/kelts.jpeg",
      link="https://www.stevenkelts.com/",
      short_org="Lecturer, Princeton University",
      active=True
    ),
    
    SpeakerProfile(
      "Arvind Narayanan",
      "Professor of Computer Science, Princeton University",
      "Arvind Narayanan is a Professor of Computer Science at Princeton University and Director of the Center for Information Technology Policy. He is the co-author of AI Snake Oil—both the book and its widely read newsletter, followed by over 50,000 researchers, policymakers, journalists, and AI enthusiasts—and previously co-authored the influential textbooks Bitcoin and Cryptocurrency Technologies and Fairness in Machine Learning. Narayanan led the Princeton Web Transparency and Accountability Project, producing landmark work on data practices and demonstrating some of the earliest evidence that machine learning systems echo cultural biases. Named to TIME’s inaugural list of the 100 most influential people in AI, he has also received the Presidential Early Career Award for Scientists and Engineers (PECASE).",
      "assets/speakers/arvind.jpg",
      link="https://www.cs.princeton.edu/~arvindn/",
      short_org="Professor, Princeton University",
      active=True
    ),
    
    

]

speakers = Speakers(SpeakerProfiles)