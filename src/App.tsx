import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { ArrowDown, ArrowLeft, ArrowRight, ArrowUpRight, Github, Menu, X } from 'lucide-react'
import { achievements, learningCourses, profile, projects, type Project } from './content'

const nav = [
  { label: 'Home', href: '#home' },
  { label: 'Introduction', href: '#welcome' },
  { label: 'About', href: '#about' },
  { label: 'Projects', href: '#projects' },
  { label: 'Achievements', href: '#achievements' },
  { label: 'Contact', href: '#contact' },
]

function routeFromHash(hash: string) {
  const route = hash.replace(/^#\/?/, '')
  if (route.startsWith('project/')) return route
  if (route === 'all-projects') return 'projects'
  if (!route) return 'welcome'
  return ['welcome', 'home', 'about', 'projects', 'achievements', 'contact'].includes(route) ? route : 'welcome'
}

function Header({ route }: { route: string }) {
  const [open, setOpen] = useState(false)
  return <header className="site-header">
    <a className="wordmark" href="#home" aria-label={`${profile.name}, home`}>
      <span className="wordmark-mark">PT</span><span>Photchara</span>
    </a>
    <button className="menu-toggle" aria-label={open ? 'Close navigation' : 'Open navigation'} aria-expanded={open} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button>
    <nav className={open ? 'nav-links is-open' : 'nav-links'} aria-label="Main navigation">
      {nav.map(item => <a className={route === item.href.slice(1) ? 'active' : ''} aria-current={route === item.href.slice(1) ? 'page' : undefined} key={item.href} href={item.href} onClick={() => setOpen(false)}>{item.label}</a>)}
    </nav>
    <a className="header-note" href="#contact"><span className="status-dot" /> COMPUTER SCIENCE · PHUKET</a>
  </header>
}

function SectionLabel({ number, children }: { number: string; children: string }) {
  return <div className="section-label"><span>{number}</span><i />{children}</div>
}

function ProjectCard({ project }: { project: Project }) {
  return <a href={`#project/${project.slug}`} className={`project-card ${project.accent}`}>
    <div className="project-top"><span className="project-number">{project.number} / {String(projects.length).padStart(2, '0')}</span><span className="project-status">{project.status}</span></div>
    <div className="project-art" aria-hidden="true"><div className="art-grid" /><div className="art-orbit orbit-one" /><div className="art-orbit orbit-two" /><span className="art-code">{project.number === '01' ? '♞' : project.number === '02' ? '⌁' : project.number === '03' ? '{ }' : '✳'}</span><span className="art-caption">FIELD NOTE · {project.number}</span></div>
    <div className="project-info"><div className="eyebrow">{project.category}</div><h3>{project.name}<ArrowUpRight size={18} /></h3><p>{project.summary}</p><div className="tag-row">{project.technologies.map(t => <span key={t}>{t}</span>)}</div></div>
  </a>
}

function HomePage() {
  return <main className="page-view home-page">
    <section className="hero section-wrap main-home-hero"><div className="hero-copy">
      <div className="eyebrow hero-eyebrow"><span className="status-dot" /> COMPUTER SCIENCE · {profile.location.toUpperCase()}</div>
      <h1>Learning Computer Science.<br /><em>Building toward AI.</em></h1>
      <p>{profile.intro}</p>
      <div className="hero-actions"><a className="button button-light" href="#projects">Explore my work <ArrowDown size={16} /></a><a className="button button-quiet" href="#about">A little about me <ArrowRight size={16} /></a></div>
    </div></section>
    <section className="intro-strip"><div className="strip-label">A NOTE ON THIS SITE</div><p>A work in progress, by design. <span>Each project is a chance to ask better questions, build with care, and share what I learn.</span></p><a href="#about">Get to know me <ArrowRight size={15} /></a></section>
    <section className="section-wrap projects-section home-projects"><div className="section-heading"><div><SectionLabel number="01">A FEW THINGS I’VE MADE</SectionLabel><h2>Learning through<br /><em>making things.</em></h2></div><p>Small projects, real source code, and an honest account of what I’m learning as I build.</p></div><div className="project-grid">{projects.slice(0, 3).map(project => <ProjectCard key={project.slug} project={project} />)}</div><a className="text-link all-projects" href="#projects">See all projects <ArrowRight size={16} /></a></section>
  </main>
}

function WelcomePage({ onContinue }: { onContinue: () => void }) {
  const [revealed, setRevealed] = useState(false)
  const firstName = profile.name.split(' ')[0]
  return <main className={`welcome-screen${revealed ? ' is-revealed' : ''}`}>
    <div className="welcome-atmosphere" aria-hidden="true">
      <div className="welcome-glow" /><div className="welcome-horizon" />
      <div className="forest-line forest-line-back">{Array.from({ length: 17 }, (_, i) => <i key={i} className={`distant-tree distant-tree-${i % 4}`} />)}</div>
      <div className="forest-line forest-line-mid">{Array.from({ length: 21 }, (_, i) => <i key={i} className={`distant-tree distant-tree-${(i + 2) % 4}`} />)}</div>
      <div className="forest-line forest-line-front">{Array.from({ length: 15 }, (_, i) => <i key={i} className={`near-tree near-tree-${i % 3}`} />)}</div>
      <div className="forest-floor" />
      <div className="forest-life forest-life-plants">{Array.from({ length: 22 }, (_, i) => <i key={i} />)}</div>
      <div className="forest-life forest-life-lights">{Array.from({ length: 12 }, (_, i) => <i key={i} />)}</div>
      <div className="welcome-tree"><i className="tree-crown crown-top"/><i className="tree-crown crown-mid"/><i className="tree-crown crown-low"/><i className="tree-trunk"/><i className="tree-root root-left"/><i className="tree-root root-right"/></div>
      <div className="welcome-grain" />
    </div>
    <button className="tree-interaction" type="button" aria-label={revealed ? "Hide introduction" : "Tap the tree to reveal the introduction"} aria-expanded={revealed} onClick={() => setRevealed(value => !value)} />
    <div className="welcome-topline"><span>COMPUTER SCIENCE PORTFOLIO</span><span>PHUKET, THAILAND</span></div>
    <div className="welcome-content"><p className="welcome-greeting">Hello, my name is</p><h1 className="welcome-name" aria-label={firstName}>{Array.from(firstName).map((letter, i) => <span key={`${letter}-${i}`} style={{ transitionDelay: `${i * 7}ms` } as CSSProperties}>{letter}</span>)}</h1><div className="welcome-surname">{profile.name.split(' ').slice(1).join(' ')}</div><p className={`welcome-description${revealed ? ' visible' : ''}`} aria-live="polite" aria-hidden={!revealed}>{profile.intro}</p><p className="welcome-quote">“Understand the roots. Build what reaches beyond them.”</p></div>
    <div className="welcome-bottom"><div className="drag-hint"><span className="drag-hint-icon">✦</span>A QUIET FOREST · TAP THE TREE TO REVEAL</div><div className="welcome-actions"><a className="welcome-button primary" href="#home" onClick={onContinue}>Continue <ArrowRight size={17} /></a><a className="welcome-button secondary" href="#projects">Explore projects <ArrowUpRight size={16} /></a></div><span className="welcome-edition">A PERSONAL LEARNING JOURNAL · 2026</span></div>
  </main>
}

function AboutPage() {
  return <main className="page-view section-wrap content-page about-page"><div className="page-intro"><SectionLabel number="01">ABOUT ME</SectionLabel><h1>Curious about how things work.<br /><em>Drawn to making them.</em></h1><p>{profile.learning}</p></div>
    <div className="about-inner about-page-inner"><div className="about-heading"><div className="eyebrow">EDUCATION & DIRECTION</div><h2>Foundations first.<br /><em>Questions always.</em></h2><p>{profile.goal}</p><a className="text-link" href="#contact">Get in touch <ArrowRight size={16} /></a></div><div className="about-list"><div className="about-item"><span>01 / EDUCATION</span><div><h3>Where I’m learning</h3><p>{profile.education}<br />{profile.school}</p></div></div><div className="about-item"><span>02 / STRENGTHS</span><div><h3>Academic interests</h3><p>{profile.strengths}</p></div></div><div className="about-item"><span>03 / NORTH STAR</span><div><h3>Where I’m headed</h3><p>{profile.goal}</p></div></div></div></div>
    <div className="page-interests"><SectionLabel number="02">THINGS I’M CURIOUS ABOUT</SectionLabel><div className="interest-grid"><article><span>01</span><h3>Algorithms<br />& structures</h3><p>Understanding how choices in representation shape the way a solution behaves.</p></article><article><span>02</span><h3>Artificial<br />intelligence</h3><p>Learning the foundations behind systems that recognize patterns and support people.</p></article><article><span>03</span><h3>Digital art<br />& dashboards</h3><p>Combining visual creativity with software to make complex, personal tools.</p></article></div></div>
  </main>
}

function ProjectsPage() {
  return <main className="page-view section-wrap content-page projects-page"><div className="page-intro"><SectionLabel number="01">PROJECTS</SectionLabel><h1>Made while<br /><em>figuring things out.</em></h1><p>Project notes draw on source files and screenshot evidence. Screenshot-only projects are labeled clearly, and their write-ups stick to what the evidence shows.</p></div><div className="project-grid all-project-cards">{projects.map(project => <ProjectCard key={project.slug} project={project} />)}</div></main>
}

const codingLanguages = ['C', 'C++', 'Python', 'Luau']

function LanguageLogo({ language }: { language: string }) {
  if (language === 'Python') return <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#3776AB" d="M14.31.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.83l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.23l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05L0 11.97l.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.24l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05 1.07.13zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09-.33.22z"/><path fill="#FFD43B" d="M21.1 6.11l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01.21.03zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08-.33.23z"/></svg>
  if (language === 'C++') return <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00599C" d="M22.393 6c-.167-.29-.398-.543-.652-.69L12.925.22c-.508-.293-1.339-.293-1.847 0L2.26 5.31c-.508.293-.923 1.013-.923 1.6v10.18c0 .294.104.62.271.91.167.29.398.543.652.689l8.816 5.091c.508.293 1.339.293 1.847 0l8.816-5.091c.254-.146.485-.399.652-.689s.271-.616.271-.91V6.91c.002-.294-.102-.62-.269-.91zM12 19.109c-3.92 0-7.109-3.189-7.109-7.109S8.08 4.891 12 4.891a7.133 7.133 0 0 1 6.156 3.552l-3.076 1.781A3.567 3.567 0 0 0 12 8.445c-1.96 0-3.554 1.595-3.554 3.555S10.04 15.555 12 15.555a3.57 3.57 0 0 0 3.08-1.778l3.077 1.78A7.135 7.135 0 0 1 12 19.109zm7.109-6.714h-.79v.79h-.79v-.79h-.79v-.79h.79v-.79h.79v.79h.79v.79zm2.962 0h-.79v.79h-.79v-.79h-.789v-.79h.789v-.79h.79v.79h.79v.79z"/></svg>
  if (language === 'Luau') return <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00A2FF" d="M24 5.072 18.928 24 0 18.928 5.072 0 24 5.072ZM8.984 18.402l-.085.375.61.163 1.005-3.75-.641-.172-.731 2.728c-.26.322-.635.417-1.125.286-.462-.124-.616-.47-.464-1.039l.649-2.422-.641-.172-.654 2.44c-.12.455-.107.828.039 1.117.148.287.422.485.822.592.483.13.888.081 1.216-.146Zm3.818 1.42.672.18.015-.055c-.034-.227-.004-.512.088-.857l.462-1.725c.093-.382.045-.713-.142-.994-.187-.282-.496-.481-.928-.597a1.897 1.897 0 0 0-.793-.05 1.42 1.42 0 0 0-.652.272.912.912 0 0 0-.343.488l.645.172c.044-.164.159-.283.344-.357a.969.969 0 0 1 .622-.02c.261.07.44.19.54.36.098.168.117.364.057.588l-.079.295-.624-.167c-.538-.145-.985-.148-1.342-.01-.353.135-.582.398-.687.789-.086.32-.04.618.14.891.183.272.458.458.828.557.414.11.811.05 1.192-.179-.028.196-.033.336-.015.42Zm-.934-.774a.8.8 0 0 1-.47-.307.606.606 0 0 1-.075-.526c.123-.46.577-.584 1.363-.374l.502.135-.206.77a.978.978 0 0 1-.5.3 1.166 1.166 0 0 1-.614.002ZM21 6.804l-3.786-1.015L16.2 9.575l3.786 1.014L21 6.804ZM3.818 16.832l1.207-4.502-.67-.18-1.352 5.047 3.06.82.146-.544-2.39-.64Zm12.944 3.654-.086.375.61.163 1.005-3.75-.641-.172-.731 2.728c-.26.322-.634.417-1.124.286-.462-.124-.617-.47-.465-1.039l.65-2.422-.642-.172-.654 2.44c-.12.456-.106.828.04 1.117.147.288.421.485.821.592.483.13.889.081 1.217-.146Z"/></svg>
  return <svg viewBox="0 0 24 24" aria-hidden="true"><text x="12" y="20" textAnchor="middle" fill="#A9D1FF" fontFamily="Arial,sans-serif" fontWeight="900" fontSize="22">C</text></svg>
}

function SkillsSection() {
  return <section className="skills-section" aria-labelledby="skills-title">
    <div className="achievement-section-heading"><SectionLabel number="03">SKILLS</SectionLabel><p id="skills-title">Programming languages I use</p></div>
    <div className="language-grid">{codingLanguages.map(language => <div className="language-item" key={language} tabIndex={0} aria-label={language} title={language}><span className={`language-logo language-${language.toLowerCase().replaceAll('+', 'p')}`}><LanguageLogo language={language} /></span><span className="language-tooltip" role="tooltip">{language}</span></div>)}</div>
  </section>
}

function LearningPage() {
  return <main className="page-view section-wrap content-page learning-page"><div className="page-intro"><SectionLabel number="01">ACHIEVEMENTS</SectionLabel><h1>Practice, participation,<br /><em>and proof.</em></h1><p>A mix of coding milestones, certificates, programming skills, and self-study evidence. Course screenshots document learning progress; they are not presented as certificates.</p></div>
    <section className="achievement-section"><div className="achievement-section-heading"><SectionLabel number="02">ACHIEVEMENTS & CERTIFICATES</SectionLabel><p>Selected milestones and evidence.</p></div><div className="achievement-grid">{achievements.map((item, i) => <article className="achievement-card" key={item.title}><a className="achievement-image" href={item.image} target="_blank" rel="noreferrer" aria-label={`${item.title} evidence`}><img src={item.image} alt={item.imageAlt} loading="lazy"/><span>OPEN EVIDENCE ↗</span></a><div className="achievement-card-copy"><div className="eyebrow">0{i + 1} · {item.type}</div><h2>{item.title}</h2><p>{item.detail}</p>{item.link && <a className="text-link" href={item.link} target="_blank" rel="noreferrer">{item.linkLabel}<ArrowUpRight size={15} /></a>}</div></article>)}</div></section>
    <SkillsSection />
    <section className="self-study-section"><div className="achievement-section-heading"><SectionLabel number="04">COURSE & SELF-STUDY EVIDENCE</SectionLabel><p>Independent learning, with no certificates claimed.</p></div><div className="study-evidence-grid">{learningCourses.map((item, i) => <article key={item.title} className="study-evidence-card"><div className="study-evidence-image">{item.image ? <a href={item.image} target="_blank" rel="noreferrer" aria-label={`${item.title} study evidence`}><img src={item.image} alt={item.imageAlt} loading="lazy"/><span>OPEN EVIDENCE ↗</span></a> : <div className="study-no-image" aria-hidden="true"><LanguageLogo language="Luau" /></div>}</div><div className="study-evidence-copy"><div className="eyebrow">0{i + 1} · {item.type}</div><h3>{item.title}</h3><p>{item.detail}</p></div></article>)}</div></section>
  </main>
}

function ContactPage() {
  return <main className="page-view contact-page"><div className="section-wrap contact-inner"><div><SectionLabel number="01">CONTACT</SectionLabel><h1>Let’s start<br />a <em>conversation.</em></h1><p>Interested in a project, a learning resource, or a Computer Science opportunity? I’d be glad to hear from you.</p><div className="contact-actions"><a className="button button-light" href={`mailto:${profile.email}`}>Email me <ArrowUpRight size={16} /></a><a className="button button-quiet" href={profile.github} target="_blank" rel="noreferrer"><Github size={16} /> GitHub <ArrowUpRight size={15} /></a></div></div><div className="contact-stamp"><span>PT</span><small>KEEP<br />GROWING</small></div></div></main>
}

function ProjectDetail({ slug }: { slug: string }) {
  const project = projects.find(item => item.slug === slug)
  if (!project) return <main className="detail-page"><a className="back-link" href="#projects"><ArrowLeft size={16} /> Back to projects</a><h1>Project not found</h1></main>
  const fields = [['The idea', project.problem], ['My contribution', project.contribution], ['How it works', project.implementation], ['A challenge', project.challenge], ['Current limits', project.limitations], ['Next steps', project.future]]
  return <main className="detail-page"><a className="back-link" href="#projects"><ArrowLeft size={16} /> Back to projects</a><div className="detail-hero"><div><div className="eyebrow">{project.number} · {project.category}</div><h1>{project.name}<em>.</em></h1><p>{project.description}</p><span className="project-status">{project.status}</span></div><div className={`detail-art ${project.accent}`} aria-hidden="true"><span>{project.number === '01' ? '♞' : project.number === '02' ? '⌁' : project.number === '03' ? '{ }' : '✳'}</span></div></div><div className="detail-grid"><aside><div className="eyebrow">TOOLS & TECHNOLOGIES</div><div className="tag-row">{project.technologies.map(technology => <span key={technology}>{technology}</span>)}</div><div className="eyebrow detail-links-title">PROJECT LINKS</div>{project.repo ? <a className="text-link" href={project.repo} target="_blank" rel="noreferrer">Repository <ArrowUpRight size={15} /></a> : <span className="muted">Repository link to be added</span>}{project.demo && <a className="text-link" href={project.demo} target="_blank" rel="noreferrer">Live demo <ArrowUpRight size={15} /></a>}</aside><div>{fields.map(([title, text], i) => <section className="detail-section" key={title}><span className="detail-index">0{i + 1}</span><div><h2>{title}</h2><p>{text}</p></div></section>)}</div></div><section className="case-media"><div className="eyebrow">SCREENSHOTS & DEMONSTRATIONS</div>{project.screenshots.length ? <div className="case-gallery">{project.screenshots.map(item => <figure key={item.src}><img src={item.src} alt={item.alt} /><figcaption>{item.alt}</figcaption></figure>)}</div> : <p>Add verified screenshots in <code>public/</code> and list their paths and alt text in <code>src/content.ts</code>.</p>}{project.demo && <a className="text-link" href={project.demo} target="_blank" rel="noreferrer">Open demonstration <ArrowUpRight size={15} /></a>}</section></main>
}

export default function App() {
  const [route, setRoute] = useState(() => routeFromHash(location.hash))
  const [playEntryIntro, setPlayEntryIntro] = useState(false)
  const entryTimer = useRef<number | null>(null)
  useEffect(() => {
    const update = () => { setRoute(routeFromHash(location.hash)); window.scrollTo({ top: 0, behavior: 'smooth' }) }
    addEventListener('hashchange', update)
    return () => removeEventListener('hashchange', update)
  }, [])
  useEffect(() => {
    if (!playEntryIntro) return
    entryTimer.current = window.setTimeout(() => setPlayEntryIntro(false), 1900)
    return () => { if (entryTimer.current !== null) window.clearTimeout(entryTimer.current) }
  }, [playEntryIntro])
  const detailSlug = route.startsWith('project/') ? route.slice('project/'.length) : null
  const pageTitles: Record<string, string> = { welcome: 'Welcome', home: 'Home', about: 'About', projects: 'Projects', achievements: 'Achievements', contact: 'Contact' }
  useEffect(() => { document.title = detailSlug ? `${projects.find(project => project.slug === detailSlug)?.name ?? 'Project'} — ${profile.name}` : `${pageTitles[route] ?? 'Portfolio'} — ${profile.name}` }, [route, detailSlug])
  if (route === 'welcome') return <WelcomePage onContinue={() => setPlayEntryIntro(true)} />
  return <><a className="skip-link" href="#main-content" onClick={event => { event.preventDefault(); document.getElementById('main-content')?.focus() }}>Skip to content</a><Header route={route} /><div id="main-content" tabIndex={-1} className={playEntryIntro && route === 'home' ? 'main-content-entering' : ''}>{detailSlug ? <ProjectDetail slug={detailSlug} /> : route === 'about' ? <AboutPage /> : route === 'projects' ? <ProjectsPage /> : route === 'achievements' ? <LearningPage /> : route === 'contact' ? <ContactPage /> : <HomePage />}</div>{playEntryIntro && route === 'home' && <div className="portfolio-intro-overlay" aria-hidden="true"><span className="intro-orbit intro-orbit-one"/><span className="intro-orbit intro-orbit-two"/><svg className="intro-tree-draw" viewBox="0 0 140 180"><path d="M70 171 C63 144 75 124 69 103 C64 82 74 62 69 32 M68 111 C53 91 40 84 23 76 M71 92 C86 72 103 63 122 57 M68 68 C53 49 43 40 29 35 M71 52 C85 37 99 30 112 27" /></svg><span className="intro-initials">PT</span><span className="intro-wordmark">PHOTCHARA · PORTFOLIO</span><span className="intro-progress"/></div>}<footer className="site-footer"><div className="footer-inner"><a className="wordmark" href="#home"><span className="wordmark-mark">PT</span><span>Photchara</span></a><span>MADE WITH CURIOSITY · {new Date().getFullYear()}</span><a href="#home">BACK TO TOP ↑</a></div></footer></>
}
