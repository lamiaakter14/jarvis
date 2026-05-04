import { MapPin, Phone, Clock, MessageCircle, Navigation } from 'lucide-react'

const contactInfo = [
  {
    icon: MapPin,
    title: 'ঠিকানা',
    lines: ['গার্লস স্কুল রোড', 'সখিপুর, টাঙ্গাইল', 'বাংলাদেশ।'],
    color: 'text-red-500',
    bg: 'bg-red-50',
  },
  {
    icon: Phone,
    title: 'ফোন',
    lines: ['+880 1X-XXXX-XXXX'],
    color: 'text-green-600',
    bg: 'bg-green-50',
    href: 'tel:+8801XXXXXXXXX',
  },
  {
    icon: Clock,
    title: 'শপ খোলার সময়',
    lines: ['শনি–বৃহস্পতি: সকাল ৮টা – রাত ১০টা', 'শুক্রবার: দুপুর ২টা – রাত ১০টা'],
    color: 'text-blue-600',
    bg: 'bg-blue-50',
  },
]

export default function Contact() {
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
            যোগাযোগ করুন
          </h1>
          <p className="text-cream/70 text-lg bn">
            যেকোনো প্রশ্ন বা অর্ডারের জন্য আমরা সবসময় প্রস্তুত
          </p>
        </div>
      </section>

      {/* Contact cards + Map */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
          {/* Left: info + WhatsApp */}
          <div>
            <div className="space-y-4 mb-8">
              {contactInfo.map((c) => {
                const Icon = c.icon
                const content = (
                  <div className={`flex gap-4 p-5 bg-white rounded-2xl shadow-brand hover:shadow-brand-lg transition-shadow ${c.href ? 'cursor-pointer' : ''}`}>
                    <div className={`w-12 h-12 ${c.bg} rounded-xl flex items-center justify-center flex-shrink-0`}>
                      <Icon className={`w-6 h-6 ${c.color}`} />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 mb-1 bn">{c.title}</h3>
                      {c.lines.map((l, i) => (
                        <p key={i} className="text-gray-600 text-sm bn">{l}</p>
                      ))}
                    </div>
                  </div>
                )
                return c.href ? (
                  <a key={c.title} href={c.href}>{content}</a>
                ) : (
                  <div key={c.title}>{content}</div>
                )
              })}
            </div>

            {/* WhatsApp CTA */}
            <div className="bg-[#25D366]/10 border-2 border-[#25D366]/30 rounded-2xl p-6 text-center">
              <MessageCircle className="w-10 h-10 text-[#25D366] mx-auto mb-3" />
              <h3 className="font-bold text-gray-900 text-lg mb-2 bn">সরাসরি WhatsApp এ অর্ডার করুন</h3>
              <p className="text-gray-600 text-sm mb-5 bn">
                দ্রুত অর্ডার করতে বা কোনো প্রশ্নের জন্য সরাসরি মেসেজ পাঠান।
              </p>
              <a
                href="https://wa.me/8801XXXXXXXXX?text=নির্ঝরণ থেকে অর্ডার করতে চাই"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-[#25D366] text-white font-semibold px-6 py-3 rounded-full hover:bg-[#1ebe5a] transition-colors bn shadow-md"
              >
                <svg viewBox="0 0 24 24" className="w-5 h-5 fill-white" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                </svg>
                WhatsApp এ মেসেজ করুন
              </a>
            </div>
          </div>

          {/* Right: Map placeholder + directions */}
          <div className="space-y-4">
            {/* Map embed placeholder */}
            <div className="rounded-2xl overflow-hidden shadow-brand h-80 bg-forest/5 relative">
              <iframe
                title="নির্ঝরণ - সখিপুর, টাঙ্গাইল"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3635.9!2d90.15!3d24.35!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sSakhipur%2C+Tangail!5e0!3m2!1sen!2sbd!4v1"
                className="w-full h-full border-0"
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              />
              {/* Overlay if no map loads */}
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-forest/5 pointer-events-none">
                <MapPin className="w-10 h-10 text-forest/30 mb-2" />
                <p className="text-forest/50 text-sm bn">গার্লস স্কুল রোড, সখিপুর</p>
              </div>
            </div>

            <a
              href="https://maps.google.com/?q=Sakhipur,Tangail,Bangladesh"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full bg-white border-2 border-forest text-forest font-semibold py-3 rounded-2xl hover:bg-forest hover:text-cream transition-all bn shadow-sm"
            >
              <Navigation className="w-4 h-4" />
              Google Maps এ দেখুন
            </a>

            {/* Instagram spot */}
            <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6 text-white text-center">
              <div className="text-4xl mb-2">📸</div>
              <h3 className="font-bold text-lg mb-1 bn">Instagram স্পট</h3>
              <p className="text-white/80 text-sm bn">
                শপে আমাদের বিশেষ কোণে এসে ছবি তুলুন।
                নির্ঝরণের লোগো ও সুন্দর লাইটিং আপনার ছবিকে করবে অসাধারণ।
              </p>
              <p className="text-white/60 text-xs mt-2 font-semibold">#নির্ঝরণ #Nirjharon #SakhipurVibes</p>
            </div>
          </div>
        </div>
      </section>

      {/* Payment info */}
      <section className="bg-cream-dark py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="section-title">পেমেন্ট ও ডেলিভারি</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-8">
            {[
              {
                emoji: '💳',
                title: 'পেমেন্ট মাধ্যম',
                items: ['বিকাশ (bKash)', 'নগদ (Nagad)', 'ক্যাশ অন ডেলিভারি'],
              },
              {
                emoji: '🛵',
                title: 'ডেলিভারি',
                items: ['সখিপুরে ১৫-২০ মিনিট', 'মিনিমাম অর্ডার: ৯৯ টাকা', 'ডেলিভারি চার্জ: ২০ টাকা'],
              },
              {
                emoji: '📦',
                title: 'প্যাকেজিং',
                items: ['ব্র্যান্ডেড প্যাকেজিং', 'থ্যাঙ্ক ইউ নোট', 'নির্ঝরণ লোগো স্টিকার'],
              },
            ].map((item) => (
              <div key={item.title} className="bg-white rounded-2xl p-6 shadow-brand">
                <div className="text-4xl mb-3">{item.emoji}</div>
                <h3 className="font-bold text-forest text-lg mb-3 bn">{item.title}</h3>
                <ul className="space-y-1.5">
                  {item.items.map((line) => (
                    <li key={line} className="text-gray-600 text-sm flex items-center gap-2 bn">
                      <span className="w-1.5 h-1.5 bg-orange-brand rounded-full flex-shrink-0" />
                      {line}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
