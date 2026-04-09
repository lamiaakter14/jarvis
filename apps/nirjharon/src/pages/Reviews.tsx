import { Star, Quote } from 'lucide-react'

interface Review {
  id: number
  name: string
  location: string
  rating: number
  text: string
  date: string
  emoji: string
  tag?: string
}

const reviews: Review[] = [
  {
    id: 1,
    name: 'রাহেলা বেগম',
    location: 'সখিপুর, টাঙ্গাইল',
    rating: 5,
    text: 'নির্ঝরণের তরমুজের জুস খেয়ে মনে হলো একদম মাঠ থেকে তুলে দিচ্ছে! এত বিশুদ্ধ জুস এর আগে কোথাও পাইনি। আর ভাপা পিঠার স্বাদ তো আমার মায়ের হাতের রান্নার কথা মনে করিয়ে দেয়।',
    date: 'জানুয়ারি ২০২৫',
    emoji: '👩',
    tag: 'নিয়মিত কাস্টমার',
  },
  {
    id: 2,
    name: 'মোঃ ফারুক হোসেন',
    location: 'সখিপুর বাজার',
    rating: 5,
    text: 'অফিসের পর প্রতিদিন এখানে আসি। কমলার জুস আর পাটিসাপ্টার কম্বো নিলে পুরো ক্লান্তি দূর হয়ে যায়। দাম একদম সাশ্রয়ী, মান অসাধারণ।',
    date: 'ফেব্রুয়ারি ২০২৫',
    emoji: '👨',
    tag: 'ডেইলি কাস্টমার',
  },
  {
    id: 3,
    name: 'সুমাইয়া আক্তার',
    location: 'গার্লস স্কুল রোড',
    rating: 5,
    text: 'এখানে দাঁড়িয়ে নিজের চোখে জুস বানাতে দেখা যায়। এটাই সবচেয়ে বড় আস্থার জায়গা। বাচ্চাদের নিয়ে আসি, ওরাও খুব পছন্দ করে।',
    date: 'মার্চ ২০২৫',
    emoji: '👩‍👦',
    tag: 'পরিবারের পছন্দ',
  },
  {
    id: 4,
    name: 'আবু সাঈদ',
    location: 'টাঙ্গাইল শহর',
    rating: 5,
    text: 'সখিপুরে এলে নির্ঝরণ না গেলে মনে হয় কিছু একটা মিস করলাম। রাজকীয় ডিটক্স জুস আমার ফেভারিট। একবার খেলে আর কোথাও যেতে মন চায় না।',
    date: 'মার্চ ২০২৫',
    emoji: '👨‍💼',
  },
  {
    id: 5,
    name: 'নাসরিন সুলতানা',
    location: 'সখিপুর',
    rating: 5,
    text: 'নকশি পিঠার সৌন্দর্য দেখে প্রথমে ছবি তুললাম, তারপর খেলাম। দুটোই অসাধারণ অভিজ্ঞতা! ইনস্টাতে পোস্ট দিলে অনেকে কমেন্ট করে কোথায় পাওয়া যায়।',
    date: 'এপ্রিল ২০২৫',
    emoji: '📸',
    tag: 'ইনস্টা ওয়ার্দি',
  },
  {
    id: 6,
    name: 'করিম ভাই',
    location: 'সখিপুর',
    rating: 5,
    text: 'ফ্যামিলি কম্বো নিলাম পুরো পরিবারের জন্য। এত সুলভে এত মান — সত্যিই অবাক করার মতো। নির্ঝরণ সখিপুরের গর্ব।',
    date: 'এপ্রিল ২০২৫',
    emoji: '👨‍👩‍👧‍👦',
    tag: 'পরিবারের পছন্দ',
  },
]

const stats = [
  { value: '৫০০+', label: 'সন্তুষ্ট কাস্টমার' },
  { value: '৪.৯', label: 'গড় রেটিং' },
  { value: '১০০%', label: 'প্রাকৃতিক উপাদান' },
  { value: '২+', label: 'বছরের অভিজ্ঞতা' },
]

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <Star
          key={i}
          className={`w-4 h-4 ${i < rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-200 fill-gray-200'}`}
        />
      ))}
    </div>
  )
}

export default function Reviews() {
  return (
    <div className="pt-16">
      {/* Header */}
      <section
        className="py-20 px-4 text-center relative overflow-hidden"
        style={{ background: 'linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)' }}
      >
        <div className="absolute inset-0 bg-leaf-pattern opacity-20" />
        <div className="relative z-10 max-w-3xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold text-cream mb-4 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
            কাস্টমার রিভিউ
          </h1>
          <p className="text-cream/70 text-lg bn">
            আমাদের কাস্টমাররাই আমাদের সেরা বিজ্ঞাপন
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-orange-brand">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
          {stats.map((s) => (
            <div key={s.label}>
              <p className="text-3xl font-bold text-white bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>{s.value}</p>
              <p className="text-white/80 text-sm mt-1 bn">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Reviews grid */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reviews.map((r) => (
            <div
              key={r.id}
              className="bg-white rounded-2xl p-6 shadow-brand hover:shadow-brand-lg transition-all hover:-translate-y-1 relative"
            >
              {/* Quote icon */}
              <Quote className="absolute top-5 right-5 w-8 h-8 text-forest/10 fill-forest/10" />

              {/* Rating */}
              <StarRating rating={r.rating} />

              {/* Text */}
              <p className="text-gray-700 text-sm leading-relaxed mt-3 mb-5 bn">{r.text}</p>

              {/* Author */}
              <div className="flex items-center gap-3 pt-4 border-t border-gray-100">
                <div className="w-10 h-10 bg-forest/10 rounded-full flex items-center justify-center text-xl">
                  {r.emoji}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-gray-900 text-sm bn">{r.name}</p>
                  <p className="text-gray-400 text-xs bn truncate">{r.location} · {r.date}</p>
                </div>
                {r.tag && (
                  <span className="text-xs bg-green-100 text-forest px-2 py-0.5 rounded-full font-medium bn flex-shrink-0">
                    {r.tag}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA – Leave a review */}
      <section
        className="py-16 px-4 text-center"
        style={{ background: 'linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)' }}
      >
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-cream mb-3 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
            আপনার অভিজ্ঞতা শেয়ার করুন
          </h2>
          <p className="text-cream/70 mb-8 bn">
            নির্ঝরণে এসেছেন? আপনার মতামত আমাদের অনুপ্রেরণা।
          </p>
          <a
            href="https://wa.me/8801XXXXXXXXX?text=আমি নির্ঝরণ সম্পর্কে আমার অভিজ্ঞতা শেয়ার করতে চাই"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary inline-flex items-center gap-2"
          >
            WhatsApp এ রিভিউ দিন
          </a>
        </div>
      </section>
    </div>
  )
}
