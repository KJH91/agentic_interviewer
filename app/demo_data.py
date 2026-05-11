"""Pre-written interview transcripts for demo / showcase purposes."""

DEMO_SCENARIOS = {
    "Software Developer": {
        "role": "Senior React Developer",
        "industry": "Software Development",
        "difficulty": "Medium",
        "interview_format": "Technical Deep-Dive",
        "description": "Technical interview for a Senior React Developer — performance, architecture, and debugging under a professional but balanced interviewer.",
        "cv_text": """James Harper
Senior Frontend Developer | 6 years experience

Skills: React, TypeScript, Next.js, Redux, Node.js, PostgreSQL, AWS (EC2, S3, Lambda), Docker, Jest, Cypress

Experience:
- Nexora Digital (2021–present): Lead frontend developer on a SaaS analytics platform serving 50,000+ users. Built React/TypeScript dashboard with real-time data visualisation. Reduced page load time by 40% through code splitting and SSR with Next.js.
- TechForge Solutions (2019–2021): Full-stack developer. Delivered 12 client projects. Introduced automated testing (Jest + Cypress), achieving 85% code coverage.

Education: BSc Computer Science, University of Manchester (2:1)
Certifications: AWS Certified Developer – Associate""",
        "job_description": """Senior React Developer — FinTrack Ltd
We are looking for a Senior React Developer to join our growing engineering team.

Requirements:
- 4+ years React experience in a production environment
- Strong TypeScript skills
- Experience with state management (Redux or Zustand)
- Familiarity with testing frameworks (Jest, Cypress or similar)
- CI/CD pipeline experience
- Comfortable working in an agile, fast-paced environment
- AWS experience desirable

Responsibilities:
- Build and maintain customer-facing React applications
- Lead code reviews and mentor junior developers
- Collaborate with product and design on feature delivery
- Contribute to architectural decisions""",
        "exchanges": [
            {
                "question": "Hello James, thanks for coming in today. I'm Alex, Senior Engineering Manager here at FinTrack. To kick us off — can you walk me through your journey into frontend development and what's kept you in it?",
                "answer": "Sure, thanks for having me. I got into frontend development during my Computer Science degree — I found that I was most energised when I could see the direct output of my work on screen. I started with vanilla JS and CSS, then picked up React in my first role at TechForge. What's kept me in it is the constant evolution — when I started nobody was talking about server components or edge rendering, and now it's central to how we think about performance. I also genuinely enjoy the collaboration with design and product — it sits at that crossroads of technical and creative which I find really engaging.",
            },
            {
                "question": "You mentioned the SaaS analytics platform at Nexora Digital. Can you tell me specifically about a performance problem you faced on that project and how you solved it?",
                "answer": "Yeah, so we had a dashboard that was rendering about 200 chart components on initial load, and time-to-interactive was around 8 seconds which was obviously terrible. I profiled the app with React DevTools and the Chrome performance panel and identified two main issues — we were loading the entire charting library upfront and we had unnecessary re-renders caused by missing memoisation. I introduced dynamic imports for the charting components, added React.memo and useMemo where the profiler showed wasted renders, and we moved the heavy data fetching to Next.js getServerSideProps so the browser received pre-computed data rather than raw records. That brought time-to-interactive down to under 2 seconds. I also set up a Lighthouse CI check in our GitHub Actions pipeline to catch regressions.",
            },
            {
                "question": "Strong answer. Let's talk about state management — one of the requirements here is Redux experience. How do you decide when Redux is the right tool versus something lighter?",
                "answer": "Honestly I think Redux gets over-used. I use it when I have genuinely global state that multiple unrelated parts of the tree need to read and write — things like authentication state, user preferences, or a shopping cart. For local or feature-scoped state I prefer useState and useReducer, or React Query if it's server state. At Nexora we started with Redux Toolkit and it was the right call because we had real-time data coming in via WebSocket that needed to be available across completely separate dashboard sections. But at TechForge I pushed back on using Redux for a smaller project and we used Context plus React Query instead, which was simpler and easier to test.",
            },
            {
                "question": "Tell me about a time you had a disagreement with a colleague about a technical approach. How did you handle it?",
                "answer": "There was a situation at Nexora where a backend engineer wanted to handle all data transformation on the frontend to avoid changing the API contract. I disagreed because it would have added significant bundle weight and made the frontend logic much harder to test. Rather than just pushing back, I put together a quick proof of concept showing the bundle size impact and wrote up a comparison doc with pros and cons of both approaches. We then had a proper discussion with the tech lead in the room. The backend engineer actually came around once they saw the numbers, and we ended up agreeing to add a lightweight transformation layer in the API gateway as a middle ground. I think the key was not making it personal and letting the data do the talking.",
            },
            {
                "question": "Last one — we're an agile team shipping weekly. How do you personally balance moving fast with maintaining code quality?",
                "answer": "I think about it in terms of what slows you down later. Skipping tests or ignoring code review feedback feels fast in the moment but creates drag that compounds over time. My approach is to be ruthless about scope — I'll push back if a ticket is trying to do too much in one sprint — and to use tooling to make quality cheap. Linting, type checking, and a solid test suite run in CI mean I'm not manually verifying things I can automate. I also find that a short PR cycle with small diffs actually moves faster than big PRs, because reviews are quicker and merge conflicts are smaller. Where I do compromise is on documentation — I'll leave a TODO and come back rather than hold up a deploy.",
            },
        ],
    },

    "Mechanic": {
        "role": "Senior Automotive Technician",
        "industry": "Automotive",
        "difficulty": "Medium",
        "interview_format": "Mixed",
        "description": "Balanced workshop interview for a Senior Automotive Technician — diagnostics, complex repairs, customer communication, and EV awareness.",
        "cv_text": """Dean Fowler
Automotive Technician | 9 years experience

Qualifications: NVQ Level 3 Vehicle Maintenance & Repair, MOT Tester Authorisation (Class 4 & 7), ADAS Calibration Certified

Skills: Diagnostics (ODIS, ISTA, Techstream), electrical fault-finding, engine overhaul, transmission repair, hybrid/EV systems awareness

Experience:
- City Ford Dealership (2018–present): Senior technician. Handle complex warranty and diagnostics jobs. Mentor two apprentices. Consistently meet or exceed workshop efficiency targets (110% average).
- Kwik Fit (2015–2018): General technician. High-volume servicing, brakes, tyres, exhausts.

Interests: Restoring a 1974 Land Rover Series III in my spare time.""",
        "job_description": """Senior Automotive Technician — Greenway Motor Group
We are recruiting an experienced technician for our busy main dealer workshop.

Requirements:
- NVQ Level 3 or equivalent
- Minimum 5 years workshop experience
- Strong diagnostic ability, especially electrical
- MOT licence desirable
- Able to work to flat-rate targets
- Good communication with service advisors and customers

Responsibilities:
- Carry out complex diagnostic and repair work
- Complete PDI inspections
- Mentor junior technicians
- Maintain workshop efficiency and quality standards""",
        "exchanges": [
            {
                "question": "Morning Dean, thanks for coming in. I'm the workshop manager here at Greenway. Tell me about your time at City Ford — what sort of work are you typically handling day-to-day?",
                "answer": "Morning, yeah so at City Ford I'm classed as a senior tech which means the foreman routes the more complex jobs to me — mainly warranty diagnostics, electrical faults, and anything the other lads haven't been able to crack. I'd say probably 60% of my week is diagnostics-led work, 30% is mechanical overhauls — gearboxes, engines — and the rest is mentoring the apprentices and doing PDIs. I also cover MOT testing a couple of days a week. It's a busy franchise dealer so we're working to flat rate and I've averaged about 110% efficiency over the last two years which I'm proud of.",
            },
            {
                "question": "Diagnostics is a big part of the role here. Walk me through how you'd approach an intermittent electrical fault — say a customer reporting random warning lights that the previous garage couldn't find.",
                "answer": "Intermittent faults are the interesting ones. First thing I do is a full scan across all modules — not just the ones with stored codes — because sometimes a fault in one area causes a symptom in another. I download the freeze frame data and look at the conditions when the fault was set. Then I'll do a visual inspection of the wiring in the affected area, checking for chafing, corrosion, or poor earth connections because that's where intermittent faults usually hide. If I can't reproduce it on a road test I'll set up live data logging on the suspect circuit and send the customer away to drive it normally. When it comes back I've got a data trail to work from. I never just clear codes and hope for the best — that wastes everyone's time.",
            },
            {
                "question": "Tell me about the most complex or challenging repair you've tackled — something that really tested you.",
                "answer": "There was a Ford Transit custom that came in with a misfire that three other garages had given up on. The customer had already had two injectors replaced elsewhere and it hadn't fixed it. I started from scratch — didn't assume the previous diagnosis was right. Full scan, checked compression, fuel pressure, everything looked normal. I put the scope on the injector waveforms and one of the injectors that hadn't been replaced was opening a fraction late — small enough that it looked okay on the basic test but the scope showed the issue clearly. Turned out there was a partial blockage in the fuel gallery to that injector rather than the injector itself. Took a full day to diagnose properly but once I had it the fix was straightforward. The customer had spent over a grand at the other garages. I think the lesson was trusting the data over assumptions.",
            },
            {
                "question": "Customer communication is important here — service advisors need to relay your findings. Tell me about a time a customer was unhappy with a repair cost or outcome.",
                "answer": "Yeah it happens. I just try to explain it simply really, so the advisor can pass it on. I'm not always great with the customer-facing side of it to be honest — I prefer to be in the workshop. But if I need to talk to a customer I just try to be straight with them.",
            },
            {
                "question": "Hybrid and electric vehicles are becoming a bigger part of our mix. What's your exposure to EV and hybrid systems?",
                "answer": "I've done the manufacturer's hybrid awareness training through Ford which covers high-voltage safety — isolation procedures, PPE, that sort of thing. I'm not yet fully qualified to work live on HV systems but I understand the fundamentals well. I've assisted on a few hybrid jobs and done some online learning through the IMI. It's an area I want to develop — I've actually looked into the IMI Level 3 EV qualification and I'd be keen for the business to support that. The diagnostic principles are similar to what I already know, it's mainly the HV safety side that needs formal sign-off.",
            },
        ],
    },

    "Nurse": {
        "role": "Registered Nurse — Adult Acute Care",
        "industry": "Healthcare",
        "difficulty": "Medium",
        "interview_format": "Behavioural Panel",
        "description": "Competency-based panel interview for a Band 6 Nursing role — prioritisation under pressure, professional escalation, and mentoring others.",
        "cv_text": """Sarah Okafor
Registered Nurse (NMC Pin: 12AB3456C) | 5 years post-qualification experience

Clinical areas: Emergency Department, Adult Acute Medical Unit
Skills: Triage, IV cannulation, medication administration, NEWS2, ABCDE assessment, venepuncture, catheterisation, ECG recording, SBAR communication

Training: ATLS (Advanced Trauma Life Support), ALERT course, Basic Life Support Instructor, Safeguarding Level 3, Mental Capacity Act trained

Experience:
- City General Hospital NHS Trust, Emergency Department (2021–present): Band 6 registered nurse. Triage lead on three shifts per week. Mentoring two student nurses and a newly qualified nurse.
- Royal West Hospital NHS Trust, AMU (2019–2021): Band 5 registered nurse. Adult acute medical care, fast-paced environment, MDT working.""",
        "job_description": """Registered Nurse (Band 6) — Acute Medical Unit, Hartwell NHS Trust

We are seeking an experienced, compassionate RN to join our 32-bed acute medical unit.

Essential:
- NMC registration (no conditions)
- Minimum 3 years post-qualification experience in an acute setting
- Experience in clinical mentorship or supervision
- Excellent communication and teamwork skills
- Ability to prioritise and work under pressure

Desirable:
- Leadership or charge nurse experience
- Prescribing qualification
- Experience with deteriorating patient management""",
        "exchanges": [
            {
                "question": "Hello Sarah, I'm the ward manager for AMU here at Hartwell. Thank you for coming in today. To start us off, can you tell me a bit about your nursing journey and what's drawn you to apply for this Band 6 role on an acute medical unit?",
                "answer": "Of course. I've been qualified for five years and spent the last three in the Emergency Department at City General, where I'm currently working at Band 6. Before that I was on AMU at Royal West as a Band 5, so I know the acute medical environment well and I genuinely love it — the variety and the pace suits me. I moved to ED to develop my clinical skills and exposure, particularly around triage and the undifferentiated patient, and I feel I've grown enormously there. But I've been reflecting on where I want to develop next and I'm drawn back to the AMU environment — the continuity of care over a shift and the MDT relationship you build. I also want to continue developing in a leadership capacity, which is why this Band 6 vacancy appeals.",
            },
            {
                "question": "Tell me about a time you had to prioritise multiple patients simultaneously when they all had competing urgent needs. What did you do and what was the outcome?",
                "answer": "Yes, a good example would be a night shift in ED a few months ago. I was triage lead and we had three patients arrive in close succession — a chest pain query MI, a patient with an acute asthma attack, and a confused elderly patient who'd had a fall and had a head injury. I quickly triaged all three using NEWS2 and ABCDE. The MI and the asthma were both clinically urgent. I escalated the MI to the resus team immediately and took the asthma patient to majors myself, starting a salbutamol nebuliser and calling the on-call medic. I delegated the head injury assessment to a senior Band 5 colleague I trusted, and briefed her clearly using SBAR. I kept checking back on all three and communicated with the team throughout. All three patients were stabilised and handed over safely. The key was not panicking, communicating clearly, and knowing my team's capabilities.",
            },
            {
                "question": "Working in acute care involves close collaboration with doctors and allied health professionals. Can you describe a situation where you had a professional disagreement with a colleague and how you managed it?",
                "answer": "There was an instance where I had concerns about a patient's deteriorating NEWS2 score and escalated to the on-call doctor, who was dismissive and said to continue monitoring. My clinical instinct said this patient needed review sooner. I used SBAR to frame my concern clearly and documented my escalation. When the doctor still didn't attend after 30 minutes and the patient's condition hadn't improved, I escalated to the registrar using our PACE tool — which is our escalation framework for exactly this situation. The registrar came, the patient turned out to be in early sepsis and was transferred to HDU. I debriefed with the ward manager the next day. I think it's important to advocate for your patient even when that's uncomfortable, and to use the systems in place rather than just accepting being brushed off.",
            },
            {
                "question": "Medication safety is critical in acute care. Can you tell me about an error or near-miss you've been involved in and what you learnt from it?",
                "answer": "I'd rather not go into specifics really. I know these things happen and I always follow the five rights of medication administration. I've never been involved in a serious error personally. I always double-check with a colleague.",
            },
            {
                "question": "This role involves mentoring junior staff. Tell me about your experience supporting others' development and your approach to it.",
                "answer": "I really enjoy the mentorship side — it's one of the reasons I'm interested in progressing. I currently mentor two student nurses and a newly qualified nurse at City General. My approach is to start by understanding where they are and what their learning goals are for the placement, rather than imposing a one-size-fits-all structure. I use a lot of real-time feedback — so if we've done a skill together I'll debrief immediately while it's fresh. I also try to model reflective practice openly, so I'll talk through my own decision-making as I go rather than just doing things. One of my student nurses recently passed her clinical skills assessment first time, which she said she'd struggled with in previous placements, and that was really rewarding. I've also done the mentorship module and I'm working towards my Practice Assessor documentation.",
            },
        ],
    },

    "Retail Worker": {
        "role": "Retail Sales Assistant",
        "industry": "Retail",
        "difficulty": "Easy",
        "interview_format": "Phone Screen",
        "description": "Friendly phone screen for an entry-level retail role — warm and conversational, covering customer service basics and motivation.",
        "cv_text": """Chloe Barnes
Retail Sales Assistant | 2.5 years experience

Skills: Customer service, cash handling, stock management, visual merchandising, POS systems (EPOS, Shopify till), returns processing

Experience:
- StyleZone (clothing retail, 2022–present): Sales assistant. Consistently ranked in top 3 for customer satisfaction scores in-store. Promoted to keyholder after 10 months. Trained 3 new starters.
- McDonald's (2021–2022): Crew member. Fast-paced customer-facing environment, cash handling.

Education: 9 GCSEs (A–C) including Maths and English""",
        "job_description": """Sales Assistant — Harlow & Co Department Store

We are looking for a friendly, motivated Sales Assistant to join our fashion floor team.

Requirements:
- Previous retail or customer service experience
- Strong communication skills
- Target-driven and proactive approach to sales
- Reliable and flexible — weekend availability required
- Smart personal presentation

Responsibilities:
- Assist customers on the shop floor and at the till
- Achieve personal and team sales targets
- Maintain stock and visual merchandising standards
- Handle returns and complaints professionally
- Support store events and promotions""",
        "exchanges": [
            {
                "question": "Hi Chloe, lovely to meet you. I'm the floor manager for fashion here at Harlow and Co. Tell me a little bit about yourself and your experience in retail so far.",
                "answer": "Hi, nice to meet you too! So I've been working at StyleZone for about two and a half years now. I started as a sales assistant and after about 10 months I was made a keyholder, which I was really proud of. In that role I help open and close the store and I'm the responsible person on shift when management aren't in. Before that I worked at McDonald's which isn't retail as such but it was really busy and customer-facing, so it gave me a lot of confidence dealing with all sorts of people. At StyleZone I've been in the top three for customer satisfaction scores pretty much every month, which is something I really care about — I want people to leave the store happy.",
            },
            {
                "question": "Customer experience is everything in our store. Can you give me a specific example of a time you went above and beyond for a customer?",
                "answer": "Yes, so there was a lady who came in looking for an outfit for her daughter's graduation. She was quite stressed and had a budget she was worried about. I spent about 45 minutes with her, pulling different options, being honest when something didn't suit her rather than just trying to make a sale. We found her a dress and a jacket that looked amazing and came in under her budget. She actually came back the following week specifically to find me and tell me her daughter had loved the outfit and she'd had so many compliments. That stuck with me because she didn't have to come back — she just wanted to say thank you. That's the kind of interaction that makes the job worthwhile.",
            },
            {
                "question": "We're quite target-driven here — the team has daily and weekly sales goals. How do you approach hitting targets?",
                "answer": "I just try my best really. I think if you're nice to customers and helpful then the sales follow naturally don't they. I don't really like the pushy sales approach, I think that puts people off. So I just focus on being helpful.",
            },
            {
                "question": "Tell me about a time you dealt with a difficult or upset customer. What happened and how did you handle it?",
                "answer": "There was a customer who came in wanting to return a dress she'd clearly worn — there was deodorant marks on it and the tags had been removed. Our policy is that we can't accept worn returns. She got quite loud and aggressive about it and said she'd never shop with us again. I stayed calm and kept my voice low because I find that helps when someone's getting louder. I apologised that she was unhappy and explained the policy clearly, and I offered to get the manager so she felt her complaint was being taken seriously. The manager agreed we couldn't process the return but offered her a discount on a future purchase as a goodwill gesture. She left unhappy but I felt we'd handled it fairly and within the policy. I made sure to write it up in the incidents book as well.",
            },
            {
                "question": "Last question — where do you see yourself in the next couple of years? What are you hoping to develop?",
                "answer": "I'd love to move into a supervisory or assistant manager role. I've already got the keyholder responsibility which has given me a taste of what it's like to be accountable for the store, and I've really enjoyed the training side of things — I've trained a few new starters and I find I'm quite good at explaining how things work. I think working in a bigger store like Harlow and Co would give me more exposure to different areas — visual merchandising, buying, events — which would help me grow. Longer term I'd like to understand the business side more, maybe do a retail management course. But I'm very happy to work my way up — I think the best managers understand the shop floor because they've done it themselves.",
            },
        ],
    },

    "Senior Project Manager": {
        "role": "Senior Project Manager",
        "industry": "Technology",
        "difficulty": "Hard",
        "interview_format": "Final Round",
        "description": "Demanding final-round interview for a VP of Delivery role — strategic thinking, team leadership, board communication, and honest self-critique under pressure.",
        "cv_text": """Rachel Chen
Senior Project Manager | 10 years experience

Certifications: PMP, PRINCE2 Practitioner, SAFe Agilist

Skills: Programme management, stakeholder engagement, Agile/Scrum/Kanban, risk management, budget ownership (£5M+), vendor management, OKR framework, JIRA, Confluence, MS Project

Experience:
- Meridian Financial Services (2020–present): Senior PM. Led digital transformation programme — migration of core banking platform for 2M+ customers. £8M budget, 60-person cross-functional team, 18-month delivery. Programme delivered on time and 4% under budget.
- Apex Consulting (2016–2020): Project Manager. Delivered 15+ projects across retail and financial services clients. Average project value £1.2M.
- DataPoint Systems (2014–2016): Junior PM / Business Analyst.

Education: MBA, Cranfield School of Management; BSc Information Systems, University of Leeds""",
        "job_description": """VP of Delivery — TechCorp Global

We are seeking an exceptional Senior Project Manager to lead our growing portfolio of enterprise technology programmes.

Requirements:
- 8+ years project/programme management experience
- Demonstrated delivery of complex, multi-stakeholder programmes (£5M+)
- Strong executive communication and board-level stakeholder management
- Experience leading cross-functional, distributed teams
- Track record of delivering business outcomes, not just outputs
- Experience with Agile and waterfall delivery methodologies

Responsibilities:
- Own end-to-end delivery of 3–5 concurrent enterprise programmes
- Build and lead a team of 4 PMs
- Drive delivery governance and reporting to C-suite
- Manage third-party vendors and partner relationships
- Contribute to strategic roadmap planning and OKR setting""",
        "exchanges": [
            {
                "question": "Rachel, welcome back — this is your final round so I'll be getting into the real substance of what you'd bring to TechCorp. You've led significant transformation programmes at Meridian. Looking back honestly, what's the one decision you made on that programme that you'd change if you could do it again?",
                "answer": "That's a fair challenge. The one I'd change is how late we brought the front-line operations team into the change management process. We had strong executive sponsorship and solid technical delivery, but we underestimated the behavioural change needed at the branch level. We ran training in the final two months before go-live, and in retrospect we should have been running engagement sessions with branch managers from month four. The adoption metrics in the first quarter post-launch were below target — we hit about 67% active usage against a 90% goal — and I attribute a significant part of that to insufficient change readiness. We recovered it by month six, but it cost us in business confidence early on. I've since embedded a formal change impact assessment into my programme initiation process.",
            },
            {
                "question": "You'd be managing four project managers in this role. Tell me about a time you had to manage a PM who was underperforming, and be specific about what you actually did.",
                "answer": "I had a PM at Apex who was technically competent but consistently struggled with stakeholder communication — status reports were late, escalations were delayed, and client satisfaction scores were sliding. My first step was a direct conversation to understand whether this was a skills gap or a motivation issue. It turned out to be confidence — she was avoiding difficult conversations with the client. We agreed a structured development plan: I did joint client calls with her for six weeks so she could observe how I handled pushback, and we did weekly debrief sessions afterwards. I also got her onto a stakeholder communication course. After three months her scores had improved materially and she went on to independently deliver her next project successfully. I think the instinct to performance-manage someone out too quickly can sometimes cost you a genuinely capable person who just needs the right investment.",
            },
            {
                "question": "At TechCorp you'd be contributing to C-suite reporting and OKR setting. How do you translate delivery status into something meaningful at board level — not RAG statuses and Gantt charts, but something that actually drives decisions?",
                "answer": "Board-level communication should be about business outcomes and the decisions this room needs to make — not delivery mechanics. When I report at executive level I frame everything around three things: where are we against the business case — not just timelines but the value we committed to deliver; what decisions do I need from this room to keep the programme on track; and what risks am I managing that they should be aware of. I actively avoid RAG slides because they create false precision — a project can be green on milestones and red on value delivery simultaneously. What I prefer is a one-page narrative with two or three call-outs: here's what's going well and why, here's what's at risk and what I'm doing about it, here's what I need from you. On OKRs, I push my team to own outcome metrics, not output metrics. A project delivered on time is an output. Customer adoption at 90% by quarter two is an outcome. I make sure every delivery milestone connects back to an OKR.",
            },
            {
                "question": "What would you do in the first 90 days at TechCorp? I want specifics, not a generic onboarding framework.",
                "answer": "Days one to thirty are about listening and building trust — not fixing things. I'd do structured conversations with each of the four PMs, the key stakeholders for each programme, and the C-suite sponsors. I want to understand not just the formal programme status but the informal dynamics — where the real risks are, where trust has been strained, what the team thinks isn't being said upwards. I'd also audit the current delivery governance framework — not to redesign it immediately, but to understand what's working. Days thirty to sixty I'd be forming views and testing them back — here's what I'm seeing, does this resonate? I'd want to make a couple of visible but low-risk improvements to build credibility. Days sixty to ninety is where I'd propose structural changes — perhaps to programme reporting cadence or how PM capacity is allocated across the portfolio. By day ninety I'd want an agreed delivery health framework with the leadership team, and one thing measurably better than when I arrived.",
            },
            {
                "question": "Final question — and I want a straight answer. Of everything you've heard about TechCorp today, what concerns you most?",
                "answer": "Genuinely — the vendor concentration risk you mentioned in the morning session. Having three programmes critically dependent on the same implementation partner without a clear exit strategy is a risk I'd want to address early. If that relationship degrades or their capacity is constrained, you have limited leverage and no fallback. I'd want to understand the contractual position, what alternative delivery capacity exists, and whether that risk is being actively managed or just acknowledged. The other thing I'll say is that the ambition of the roadmap is exciting, but I'd want an honest conversation about whether the current PM team has the bandwidth to absorb the planned intake. Growth is a risk as well as an opportunity, and burning out four experienced PMs in year one would set the whole portfolio back. Those aren't reasons not to join — they're the first two things I'd address.",
            },
        ],
    },
}
