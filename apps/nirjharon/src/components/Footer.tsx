import { Link } from 'react-router-dom'
import { Leaf, MapPin, Phone, Facebook, Instagram, Youtube } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-forest text-cream">
      {/* Top section */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
        {/* Brand */}
        <div className="lg:col-span-1">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-10 h-10 bg-orange-brand rounded-full flex items-center justify-center">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-xl font-bold bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>নির্ঝরণ</p>
              <p className="text-orange-light text-xs tracking-widest uppercase" style={{ fontFamily: 'Lato, sans-serif' }}>Nirjharon</p>
            </div>
          </div>
          <p className="text-cream/70 text-sm leading-relaxed bn">
            প্রকৃতির সতেজতা, ঐতিহ্যের স্বাদ।
            সখিপুরের প্রথম প্রিমিয়াম জুস বার এবং ঐতিহ্যের পিঠা ঘর।
          </p>
          <div className="flex gap-3 mt-5">
            <a href="#" aria-label="Facebook" className="w-9 h-9 bg-cream/10 rounded-full flex items-center justify-center hover:bg-orange-brand transition-colors">
              <Facebook className="w-4 h-4" />
            </a>
            <a href="#" aria-label="Instagram" className="w-9 h-9 bg-cream/10 rounded-full flex items-center justify-center hover:bg-orange-brand transition-colors">
              <Instagram className="w-4 h-4" />
            </a>
            <a href="#" aria-label="YouTube" className="w-9 h-9 bg-cream/10 rounded-full flex items-center justify-center hover:bg-orange-brand transition-colors">
              <Youtube className="w-4 h-4" />
            </a>
          </div>
        </div>

        {/* Quick Links */}
        <div>
          <h4 className="font-bold text-orange-light mb-4 bn text-lg">দ্রুত লিংক</h4>
          <ul className="space-y-2 text-sm text-cream/70">
            {[
              { to: '/', label: 'হোম' },
              { to: '/menu', label: 'মেনু' },
              { to: '/story', label: 'আমাদের গল্প' },
              { to: '/reviews', label: 'কাস্টমার রিভিউ' },
              { to: '/contact', label: 'যোগাযোগ' },
            ].map((l) => (
              <li key={l.to}>
                <Link to={l.to} className="hover:text-orange-brand transition-colors bn">
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Contact */}
        <div>
          <h4 className="font-bold text-orange-light mb-4 bn text-lg">যোগাযোগ</h4>
          <ul className="space-y-3 text-sm text-cream/70">
            <li className="flex gap-3">
              <MapPin className="w-4 h-4 text-orange-brand mt-0.5 flex-shrink-0" />
              <span className="bn">গার্লস স্কুল রোড, সখিপুর, টাঙ্গাইল।</span>
            </li>
            <li className="flex gap-3">
              <Phone className="w-4 h-4 text-orange-brand mt-0.5 flex-shrink-0" />
              <a href="tel:+8801XXXXXXXXX" className="hover:text-orange-brand transition-colors">
                +880 1X-XXXX-XXXX
              </a>
            </li>
          </ul>
          <div className="mt-5">
            <p className="text-xs text-cream/50 mb-2 bn">শপ খোলার সময়</p>
            <p className="text-sm text-cream/80 bn">শনি–বৃহস্পতি: সকাল ৮টা – রাত ১০টা</p>
            <p className="text-sm text-cream/80 bn">শুক্রবার: দুপুর ২টা – রাত ১০টা</p>
          </div>
        </div>

        {/* Payment & Trust */}
        <div>
          <h4 className="font-bold text-orange-light mb-4 bn text-lg">পেমেন্ট পদ্ধতি</h4>
          <div className="flex flex-wrap gap-2">
            <div className="bg-cream/10 border border-cream/20 rounded-xl px-4 py-2.5 text-center">
              <p className="text-lg font-bold text-pink-400">bKash</p>
              <p className="text-xs text-cream/60 bn">বিকাশ</p>
            </div>
            <div className="bg-cream/10 border border-cream/20 rounded-xl px-4 py-2.5 text-center">
              <p className="text-lg font-bold text-orange-400">Nagad</p>
              <p className="text-xs text-cream/60 bn">নগদ</p>
            </div>
            <div className="bg-cream/10 border border-cream/20 rounded-xl px-4 py-2.5 text-center">
              <p className="text-sm font-bold text-blue-300">Cash</p>
              <p className="text-xs text-cream/60 bn">ক্যাশ</p>
            </div>
          </div>
          <div className="mt-5 space-y-2 text-xs text-cream/50">
            <p className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-orange-brand rounded-full inline-block" />
              <span className="bn">১০০% প্রাকৃতিক উপাদান</span>
            </p>
            <p className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-orange-brand rounded-full inline-block" />
              <span className="bn">কেমিক্যাল ও প্রিজার্ভেটিভ মুক্ত</span>
            </p>
            <p className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-orange-brand rounded-full inline-block" />
              <span className="bn">হোম ডেলিভারি সুবিধা</span>
            </p>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-cream/10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-cream/40">
          <p className="bn">© ২০২৪ নির্ঝরণ। সর্বস্বত্ব সংরক্ষিত।</p>
          <p>nirjharon.com · Sakhipur, Tangail</p>
        </div>
      </div>
    </footer>
  )
}
