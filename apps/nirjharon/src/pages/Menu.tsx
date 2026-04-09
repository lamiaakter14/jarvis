import { useState } from 'react'
import { ShoppingBag } from 'lucide-react'

type Category = 'all' | 'juice' | 'pitha' | 'combo' | 'premium'

interface MenuItem {
  id: string
  category: Exclude<Category, 'all'>
  emoji: string
  name: string
  nameLatin: string
  desc: string
  price: number
  oldPrice?: number
  isPopular?: boolean
  isNew?: boolean
  isVeg?: boolean
}

const menuItems: MenuItem[] = [
  // ── Juices ──
  {
    id: 'j1', category: 'juice', emoji: '🍊',
    name: 'তাজা কমলার জুস', nameLatin: 'Fresh Orange Juice',
    desc: 'রোজ সকালে সংগ্রহ করা টাটকা কমলা থেকে তৈরি।',
    price: 79, isPopular: true, isVeg: true,
  },
  {
    id: 'j2', category: 'juice', emoji: '🍉',
    name: 'তরমুজের জুস', nameLatin: 'Watermelon Juice',
    desc: 'গরমে ঠান্ডা তরমুজের রস — একটুকরো সতেজতা।',
    price: 69, isVeg: true,
  },
  {
    id: 'j3', category: 'juice', emoji: '🍓',
    name: 'মিক্সড ফ্রুট জুস', nameLatin: 'Mixed Fruit Juice',
    desc: 'কমলা, আম, স্ট্রবেরি ও আঙুরের অনন্য মিশ্রণ।',
    price: 99, oldPrice: 119, isPopular: true, isVeg: true,
  },
  {
    id: 'j4', category: 'juice', emoji: '🌿',
    name: 'আখের রস', nameLatin: 'Sugarcane Juice',
    desc: 'সরাসরি আখ থেকে চেপে নেওয়া টাটকা রস, লেবু ও আদা সহ।',
    price: 49, isVeg: true,
  },
  {
    id: 'j5', category: 'juice', emoji: '🥥',
    name: 'ডাবের পানি', nameLatin: 'Coconut Water',
    desc: 'তাজা সবুজ ডাব ভেঙে পরিবেশন।',
    price: 59, isVeg: true,
  },
  {
    id: 'j6', category: 'juice', emoji: '🍏',
    name: 'সবুজ আপেলের জুস', nameLatin: 'Green Apple Juice',
    desc: 'সবুজ আপেল ও আদার মিশ্রণে তৈরি ডিটক্স ড্রিংক।',
    price: 89, isNew: true, isVeg: true,
  },
  {
    id: 'j7', category: 'juice', emoji: '🥭',
    name: 'রাজকীয় ডিটক্স জুস', nameLatin: 'Royal Detox Juice',
    desc: 'আম, আদা, লেবু ও পুদিনার মিশ্রণে তৈরি অপূর্ব ডিটক্স জুস।',
    price: 119, oldPrice: 149, isPopular: true, isVeg: true,
  },

  // ── Pithas ──
  {
    id: 'p1', category: 'pitha', emoji: '🫓',
    name: 'ভাপা পিঠা', nameLatin: 'Bhapa Pitha',
    desc: 'গোলাপ ফুলের মতো নরম, নারিকেলের পুর দিয়ে তৈরি তুষের ভাপা পিঠা।',
    price: 39, isPopular: true, isVeg: true,
  },
  {
    id: 'p2', category: 'pitha', emoji: '🥞',
    name: 'চিতই পিঠা', nameLatin: 'Chitoi Pitha',
    desc: 'সরিষা বাটা ও গুড়ের সাথে পরিবেশন করা ঐতিহ্যবাহী চিতই।',
    price: 29, isVeg: true,
  },
  {
    id: 'p3', category: 'pitha', emoji: '🌯',
    name: 'পাটিসাপ্টা', nameLatin: 'Patishapta',
    desc: 'নারিকেল ও গুড়ের পুর দিয়ে পাতলা রুটিতে মোড়ানো।',
    price: 49, isPopular: true, isVeg: true,
  },
  {
    id: 'p4', category: 'pitha', emoji: '🔵',
    name: 'পুলি পিঠা', nameLatin: 'Puli Pitha',
    desc: 'চালের গুঁড়ার খোলসে নারিকেলের পুর দিয়ে সিদ্ধ করা পিঠা।',
    price: 39, isVeg: true,
  },
  {
    id: 'p5', category: 'pitha', emoji: '🎨',
    name: 'নকশি পিঠা', nameLatin: 'Nakshi Pitha',
    desc: 'হাতে খোদাই করা অনন্য নকশায় তৈরি ঐতিহ্যবাহী পিঠা।',
    price: 59, isNew: true, isVeg: true,
  },
  {
    id: 'p6', category: 'pitha', emoji: '🍯',
    name: 'মালপোয়া', nameLatin: 'Malpoa',
    desc: 'চিনির রসে ডোবানো নরম ময়দার পিঠা।',
    price: 45, isVeg: true,
  },

  // ── Combos ──
  {
    id: 'c1', category: 'combo', emoji: '🍹',
    name: 'জুস + পিঠা কম্বো', nameLatin: 'Juice & Pitha Combo',
    desc: 'যেকোনো ১টি জুস + ২টি পিঠা একসাথে।',
    price: 149, oldPrice: 179, isPopular: true,
  },
  {
    id: 'c2', category: 'combo', emoji: '👨‍👩‍👧‍👦',
    name: 'ফ্যামিলি কম্বো', nameLatin: 'Family Combo',
    desc: '৪টি জুস + ৮টি পিঠা — পরিবারের জন্য সেরা প্যাকেজ।',
    price: 499, oldPrice: 599,
  },
  {
    id: 'c3', category: 'combo', emoji: '💑',
    name: 'কাপল স্পেশাল', nameLatin: 'Couple Special',
    desc: '২টি প্রিমিয়াম জুস + ৪টি পিঠা — ডেটের জন্য পার্ফেক্ট।',
    price: 249, oldPrice: 299,
  },

  // ── Premium ──
  {
    id: 'pr1', category: 'premium', emoji: '👑',
    name: 'রাজকীয় প্লেটার', nameLatin: 'Royal Platter',
    desc: '৬ ধরনের পিঠা + ২টি স্পেশাল জুস + ডাব — সর্বোচ্চ অভিজ্ঞতা।',
    price: 699, oldPrice: 849,
  },
  {
    id: 'pr2', category: 'premium', emoji: '🌿',
    name: 'ডিটক্স হেলথ প্যাকেজ', nameLatin: 'Detox Health Package',
    desc: 'সপ্তাহের ৭টি ভিন্ন স্বাস্থ্যকর জুস — হেলথ কনশাসদের জন্য।',
    price: 549, isNew: true,
  },
]

const tabs: { key: Category; label: string; emoji: string }[] = [
  { key: 'all', label: 'সব', emoji: '✨' },
  { key: 'juice', label: 'জুস', emoji: '🍊' },
  { key: 'pitha', label: 'পিঠা', emoji: '🫓' },
  { key: 'combo', label: 'কম্বো', emoji: '🎁' },
  { key: 'premium', label: 'প্রিমিয়াম', emoji: '👑' },
]

function formatPrice(p: number) {
  // Convert to Bengali numerals
  const bnDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
  return String(p)
    .split('')
    .map((d) => (d >= '0' && d <= '9' ? bnDigits[parseInt(d)] : d))
    .join('')
}

export default function Menu() {
  const [active, setActive] = useState<Category>('all')

  const filtered =
    active === 'all' ? menuItems : menuItems.filter((i) => i.category === active)

  return (
    <div className="pt-16">
      {/* Header */}
      <section
        className="py-16 px-4 text-center"
        style={{ background: 'linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)' }}
      >
        <h1 className="text-4xl md:text-5xl font-bold text-cream mb-3 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
          আমাদের মেনু
        </h1>
        <p className="text-cream/70 text-lg bn">
          ১০০% প্রাকৃতিক উপাদানে তৈরি — কোনো কেমিক্যাল নেই
        </p>
      </section>

      {/* Tabs */}
      <section className="sticky top-16 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex gap-1 overflow-x-auto py-3 scrollbar-hide">
            {tabs.map((t) => (
              <button
                key={t.key}
                onClick={() => setActive(t.key)}
                className={`flex items-center gap-1.5 px-5 py-2.5 rounded-full text-sm font-medium whitespace-nowrap transition-all bn ${
                  active === t.key
                    ? 'bg-forest text-cream shadow-sm'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <span>{t.emoji}</span>
                {t.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Items */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((item) => (
            <div key={item.id} className="card-product group">
              {/* Emoji area */}
              <div className="h-40 bg-gradient-to-br from-forest/5 to-orange-brand/5 flex items-center justify-center relative">
                <span className="text-6xl group-hover:scale-110 transition-transform duration-300">
                  {item.emoji}
                </span>
                {/* Badges */}
                <div className="absolute top-3 left-3 flex flex-col gap-1.5">
                  {item.isPopular && (
                    <span className="badge-popular">🔥 জনপ্রিয়</span>
                  )}
                  {item.isNew && (
                    <span className="badge-fresh">✨ নতুন</span>
                  )}
                </div>
                {item.isVeg && (
                  <div className="absolute top-3 right-3 w-6 h-6 bg-green-500 rounded-sm flex items-center justify-center">
                    <div className="w-3 h-3 bg-white rounded-full" />
                  </div>
                )}
              </div>

              <div className="p-5">
                <h3 className="font-bold text-gray-900 text-base bn leading-snug">{item.name}</h3>
                <p className="text-gray-400 text-xs mt-0.5 mb-2 italic">{item.nameLatin}</p>
                <p className="text-gray-600 text-sm mb-4 leading-relaxed bn">{item.desc}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-baseline gap-1.5">
                    <span className="price-tag">৳{formatPrice(item.price)}</span>
                    {item.oldPrice && (
                      <span className="strike-price">৳{formatPrice(item.oldPrice)}</span>
                    )}
                  </div>
                  <a
                    href={`https://wa.me/8801XXXXXXXXX?text=${encodeURIComponent(`${item.name} অর্ডার করতে চাই`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 text-sm bg-forest text-cream px-4 py-2 rounded-full hover:bg-forest-light transition-colors bn"
                  >
                    <ShoppingBag className="w-3.5 h-3.5" />
                    অর্ডার
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Payment methods */}
        <div className="mt-14 bg-white rounded-3xl p-8 shadow-brand text-center">
          <h3 className="text-xl font-bold text-forest mb-2 bn">পেমেন্ট পদ্ধতি</h3>
          <p className="text-gray-500 text-sm mb-6 bn">আমরা নিম্নলিখিত পেমেন্ট মাধ্যম গ্রহণ করি</p>
          <div className="flex flex-wrap justify-center gap-4">
            {[
              { name: 'bKash', color: 'text-pink-500', bg: 'bg-pink-50', border: 'border-pink-200' },
              { name: 'Nagad', color: 'text-orange-500', bg: 'bg-orange-50', border: 'border-orange-200' },
              { name: 'ক্যাশ', color: 'text-green-700', bg: 'bg-green-50', border: 'border-green-200' },
            ].map((p) => (
              <div
                key={p.name}
                className={`${p.bg} ${p.border} border-2 rounded-2xl px-6 py-3`}
              >
                <span className={`text-xl font-bold ${p.color} bn`}>{p.name}</span>
              </div>
            ))}
          </div>
          <p className="text-gray-400 text-xs mt-4 bn">
            * সকল মূল্য বাংলাদেশী টাকায়। ট্যাক্স ও চার্জসহ মূল্য।
          </p>
        </div>
      </section>
    </div>
  )
}
