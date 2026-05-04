import { useState, useEffect } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { Menu, X, Leaf } from 'lucide-react'

const navLinks = [
  { to: '/', label: 'হোম' },
  { to: '/menu', label: 'মেনু' },
  { to: '/story', label: 'আমাদের গল্প' },
  { to: '/reviews', label: 'রিভিউ' },
  { to: '/contact', label: 'যোগাযোগ' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-white/95 backdrop-blur-sm shadow-brand'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link
          to="/"
          className="flex items-center gap-2 group"
          onClick={() => setOpen(false)}
        >
          <div className="w-9 h-9 bg-forest rounded-full flex items-center justify-center shadow-sm group-hover:bg-forest-light transition-colors">
            <Leaf className="w-5 h-5 text-cream" />
          </div>
          <div className="leading-tight">
            <span className="block text-forest font-bold text-lg bn" style={{ fontFamily: 'Hind Siliguri, sans-serif', lineHeight: 1.2 }}>
              নির্ঝরণ
            </span>
            <span className="block text-orange-brand text-[10px] font-semibold tracking-widest uppercase" style={{ fontFamily: 'Lato, sans-serif' }}>
              Nirjharon
            </span>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === '/'}
              className={({ isActive }) =>
                `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 bn ${
                  isActive
                    ? 'bg-forest text-cream'
                    : `${scrolled ? 'text-gray-700' : 'text-forest'} hover:bg-forest/10`
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
          <a
            href="https://wa.me/8801XXXXXXXXX"
            target="_blank"
            rel="noopener noreferrer"
            className="ml-2 btn-primary text-sm py-2 px-5"
          >
            অর্ডার করুন
          </a>
        </nav>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2 rounded-lg text-forest hover:bg-forest/10 transition-colors"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-white border-t border-gray-100 shadow-lg animate-fade-in">
          <nav className="max-w-6xl mx-auto px-4 py-4 flex flex-col gap-1">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/'}
                className={({ isActive }) =>
                  `px-4 py-3 rounded-xl text-base font-medium transition-all bn ${
                    isActive
                      ? 'bg-forest text-cream'
                      : 'text-gray-700 hover:bg-forest/10'
                  }`
                }
                onClick={() => setOpen(false)}
              >
                {link.label}
              </NavLink>
            ))}
            <a
              href="https://wa.me/8801XXXXXXXXX"
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 btn-primary text-center"
              onClick={() => setOpen(false)}
            >
              অর্ডার করুন
            </a>
          </nav>
        </div>
      )}
    </header>
  )
}
