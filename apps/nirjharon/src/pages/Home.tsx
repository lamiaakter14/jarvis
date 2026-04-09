import { Link } from 'react-router-dom'
import { ArrowRight, Sparkles, ChevronDown } from 'lucide-react'
import TrustBadges from '../components/TrustBadges'
import CountdownTimer from '../components/CountdownTimer'

const categories = [
  {
    emoji: '🍊',
    title: 'ফ্রেশ জুস',
    desc: 'সিজনাল ফলের তাজা রস',
    color: 'from-orange-400 to-orange-600',
    href: '/menu#juice',
  },
  {
    emoji: '🫓',
    title: 'পিঠা-পুলি',
    desc: 'ঘরের স্বাদের দেশীয় পিঠা',
    color: 'from-forest to-forest-light',
    href: '/menu#pitha',
  },
  {
    emoji: '🎁',
    title: 'কম্বো ডিল',
    desc: 'জুস + পিঠা একসাথে সাশ্রয়ে',
    color: 'from-purple-500 to-purple-700',
    href: '/menu#combo',
  },
  {
    emoji: '👑',
    title: 'প্রিমিয়াম',
    desc: 'রাজকীয় স্পেশাল প্যাকেজ',
    color: 'from-yellow-500 to-yellow-700',
    href: '/menu#premium',
  },
]

const featuredItems = [
  {
    name: 'রাজকীয় ডিটক্স জুস',
    nameLatin: 'Royal Detox Juice',
    price: '১১৯',
    oldPrice: '১৪৯',
    badge: 'বেস্ট সেলার',
    emoji: '🥭',
    desc: 'আম, আদা, লেবু ও পুদিনার মিশ্রণে তৈরি অপূর্ব ডিটক্স জুস।',
    isPopular: true,
  },
  {
    name: 'ভাপা পিঠা স্পেশাল',
    nameLatin: 'Bhapa Pitha Special',
    price: '৪৯',
    oldPrice: null,
    badge: 'ঐতিহ্যবাহী',
    emoji: '🫓',
    desc: 'গোলাপ ফুলের মতো নরম, নারিকেলের পুর দিয়ে তৈরি তুষের ভাপা পিঠা।',
    isPopular: false,
  },
  {
    name: 'জুস + পিঠা কম্বো',
    nameLatin: 'Juice & Pitha Combo',
    price: '১৪৯',
    oldPrice: '১৭৯',
    badge: '১৬% ছাড়',
    emoji: '🍹',
    desc: 'যেকোনো একটি জুস ও দুটি পিঠা একসাথে — সেরা কম্বো অফার!',
    isPopular: true,
  },
]

export default function Home() {
  return (
    <div className="pt-16">
      {/* ─── Hero ─── */}
      <section
        className="relative min-h-screen flex flex-col items-center justify-center text-center px-4 overflow-hidden"
        style={{
          background: 'linear-gradient(135deg, #0D2B1F 0%, #1B4332 50%, #2D6A4F 100%)',
        }}
      >
        {/* Decorative circles */}
        <div className="absolute top-20 left-10 w-64 h-64 bg-orange-brand/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-orange-brand/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl mx-auto animate-fade-in">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-orange-brand/20 border border-orange-brand/40 text-orange-light rounded-full px-4 py-1.5 text-sm mb-6 bn">
            <Sparkles className="w-4 h-4" />
            সখিপুরের প্রথম প্রিমিয়াম জুস বার
          </div>

          {/* Brand name */}
          <h1 className="text-7xl md:text-8xl font-bold text-cream mb-2 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif', letterSpacing: '-0.02em' }}>
            নির্ঝরণ
          </h1>
          <p className="text-orange-light tracking-[0.3em] text-sm font-semibold uppercase mb-4" style={{ fontFamily: 'Lato, sans-serif' }}>
            N I R J H A R O N
          </p>

          <p className="text-cream/80 text-xl md:text-2xl mb-10 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
            "প্রকৃতির সতেজতা, ঐতিহ্যের স্বাদ।"
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
            <Link to="/menu" className="btn-primary flex items-center gap-2">
              মেনু দেখুন
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="https://wa.me/8801XXXXXXXXX"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary flex items-center gap-2 border-cream/40 text-cream hover:bg-cream/10 hover:border-cream"
            >
              সরাসরি অর্ডার করুন
            </a>
          </div>

          {/* Countdown */}
          <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-6 inline-block">
            <p className="text-orange-light text-sm font-semibold mb-3 bn">⏰ আজকের স্পেশাল অফার</p>
            <CountdownTimer targetTime="22:00" label="অফার শেষ হতে বাকি" />
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce-gentle text-cream/40">
          <ChevronDown className="w-6 h-6" />
        </div>
      </section>

      {/* ─── Trust Badges ─── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-12 -mt-6 relative z-10">
        <TrustBadges />
      </section>

      {/* ─── Categories ─── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        <div className="text-center mb-10">
          <h2 className="section-title">আমাদের বিশেষত্ব</h2>
          <p className="section-subtitle bn">১০০% প্রাকৃতিক উপাদানে তৈরি, কোনো কৃত্রিম রং বা সংরক্ষক নেই</p>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.title}
              to={cat.href}
              className="group relative rounded-3xl overflow-hidden h-48 flex flex-col justify-end p-5 cursor-pointer"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${cat.color} opacity-90 group-hover:opacity-100 transition-opacity`} />
              <div className="relative z-10">
                <span className="text-4xl block mb-2 group-hover:scale-110 transition-transform duration-300">{cat.emoji}</span>
                <h3 className="text-white font-bold text-lg bn">{cat.title}</h3>
                <p className="text-white/70 text-xs mt-0.5 bn">{cat.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ─── Featured Items ─── */}
      <section className="bg-cream-dark py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-10">
            <h2 className="section-title">ফিচার্ড আইটেম</h2>
            <p className="section-subtitle bn">আমাদের সবচেয়ে জনপ্রিয় পছন্দগুলো</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featuredItems.map((item) => (
              <div key={item.name} className="card-product group">
                {/* Image area */}
                <div className="h-44 bg-gradient-to-br from-forest/10 to-orange-brand/10 flex items-center justify-center relative overflow-hidden">
                  <span className="text-7xl group-hover:scale-110 transition-transform duration-300">{item.emoji}</span>
                  <span className={`absolute top-3 left-3 text-xs font-bold px-3 py-1 rounded-full ${item.isPopular ? 'bg-orange-brand text-white' : 'bg-forest text-cream'} bn`}>
                    {item.badge}
                  </span>
                </div>
                {/* Content */}
                <div className="p-5">
                  <h3 className="font-bold text-gray-900 text-lg bn">{item.name}</h3>
                  <p className="text-gray-500 text-xs mt-0.5 mb-3">{item.nameLatin}</p>
                  <p className="text-gray-600 text-sm mb-4 bn leading-relaxed">{item.desc}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-baseline gap-1">
                      <span className="price-tag">৳{item.price}</span>
                      {item.oldPrice && <span className="strike-price">৳{item.oldPrice}</span>}
                    </div>
                    <a
                      href="https://wa.me/8801XXXXXXXXX"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm bg-forest text-cream px-4 py-2 rounded-full hover:bg-forest-light transition-colors bn"
                    >
                      অর্ডার
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="text-center mt-10">
            <Link to="/menu" className="btn-primary inline-flex items-center gap-2">
              সম্পূর্ণ মেনু দেখুন
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* ─── Open Counter CTA ─── */}
      <section
        className="py-16 px-4 text-center"
        style={{ background: 'linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)' }}
      >
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-cream mb-4 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
            আপনার চোখের সামনে তৈরি হয়
          </h2>
          <p className="text-cream/70 text-lg bn mb-8">
            আমাদের ওপেন কাউন্টারে আপনি নিজে দেখতে পাবেন কীভাবে প্রতিটি জুস তাজা ফল থেকে তৈরি হচ্ছে।
            স্বচ্ছতাই আমাদের সেরা বিজ্ঞাপন।
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/story" className="btn-secondary border-cream/40 text-cream hover:bg-cream/10 hover:border-cream">
              আমাদের গল্প পড়ুন
            </Link>
            <Link to="/contact" className="btn-primary">
              আমাদের খুঁজে পান
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
