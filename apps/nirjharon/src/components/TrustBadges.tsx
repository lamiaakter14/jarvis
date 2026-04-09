import { ShieldCheck, Leaf, Truck, Star } from 'lucide-react'

const badges = [
  {
    icon: Leaf,
    title: '১০০% প্রাকৃতিক',
    desc: 'কোনো কেমিক্যাল নেই',
    color: 'text-forest',
    bg: 'bg-green-50',
  },
  {
    icon: ShieldCheck,
    title: 'বিশুদ্ধতার গ্যারান্টি',
    desc: 'প্রিজার্ভেটিভ মুক্ত',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
  },
  {
    icon: Truck,
    title: 'দ্রুত ডেলিভারি',
    desc: 'সখিপুরে ১৫–২০ মিনিট',
    color: 'text-orange-brand',
    bg: 'bg-orange-50',
  },
  {
    icon: Star,
    title: 'সেরা মান',
    desc: 'কাস্টমারদের ১ম পছন্দ',
    color: 'text-yellow-600',
    bg: 'bg-yellow-50',
  },
]

export default function TrustBadges() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {badges.map((b) => {
        const Icon = b.icon
        return (
          <div
            key={b.title}
            className="flex items-start gap-3 p-4 rounded-2xl bg-white shadow-brand hover:shadow-brand-lg transition-shadow"
          >
            <div className={`w-10 h-10 ${b.bg} rounded-xl flex items-center justify-center flex-shrink-0`}>
              <Icon className={`w-5 h-5 ${b.color}`} />
            </div>
            <div>
              <p className="font-semibold text-gray-800 text-sm bn leading-tight">{b.title}</p>
              <p className="text-gray-500 text-xs mt-0.5 bn">{b.desc}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}
