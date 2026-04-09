import { Leaf, Heart, Users, Award } from 'lucide-react'

const milestones = [
  { year: '২০২২', title: 'স্বপ্নের শুরু', desc: 'সখিপুরে রাস্তার ধারে একটি ছোট জুসের স্টল থেকে শুরু।' },
  { year: '২০২৩', title: 'পিঠার সংযোজন', desc: 'ঐতিহ্যবাহী পিঠার সাথে জুস মিলিয়ে অনন্য অভিজ্ঞতা তৈরি।' },
  { year: '২০২৪', title: 'নির্ঝরণের জন্ম', desc: 'স্থায়ী শপ খুলে "নির্ঝরণ" ব্র্যান্ড হিসেবে যাত্রা শুরু।' },
  { year: '২০২৫', title: 'অনলাইন সম্প্রসারণ', desc: 'হোম ডেলিভারি ও অনলাইন অর্ডার শুরু।' },
]

const values = [
  {
    icon: Leaf,
    title: 'বিশুদ্ধতা',
    desc: 'প্রতিটি ফল ও উপাদান সরাসরি কৃষক থেকে সংগ্রহ করা হয়। কোনো কৃত্রিম রং, সংরক্ষক বা কেমিক্যাল ব্যবহার করা হয় না।',
    color: 'bg-green-50 text-forest',
  },
  {
    icon: Heart,
    title: 'ভালোবাসা',
    desc: 'প্রতিটি জুস ও পিঠা তৈরি হয় মায়ের হাতের রান্নার মতো যত্ন নিয়ে। খাবার শুধু পেট ভরায় না, মনও ভরায়।',
    color: 'bg-red-50 text-red-600',
  },
  {
    icon: Users,
    title: 'সম্প্রদায়',
    desc: 'আমরা স্থানীয় কৃষক ও উদ্যোক্তাদের সাথে কাজ করি। প্রতিটি কেনাকাটায় আপনি স্থানীয় অর্থনীতিতে অবদান রাখছেন।',
    color: 'bg-blue-50 text-blue-600',
  },
  {
    icon: Award,
    title: 'মান',
    desc: 'সখিপুরে সর্বোচ্চ মানের জুস ও পিঠা পরিবেশন করার প্রতিশ্রুতি আমাদের সবচেয়ে বড় গর্ব।',
    color: 'bg-yellow-50 text-yellow-700',
  },
]

export default function Story() {
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
            আমাদের গল্প
          </h1>
          <p className="text-cream/70 text-lg bn leading-relaxed">
            একটি ছোট্ট স্বপ্ন থেকে সখিপুরের মানুষের হৃদয়ে
          </p>
        </div>
      </section>

      {/* Story prose */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 py-16">
        <div className="prose prose-lg max-w-none">
          <div className="bg-cream-dark rounded-3xl p-8 md:p-12 mb-12 relative">
            <div className="absolute -top-5 left-10 text-8xl opacity-20 text-forest select-none" aria-hidden>❝</div>
            <p className="text-gray-700 text-lg leading-relaxed bn relative z-10">
              আমি যখন ছোট ছিলাম, প্রতি শীতে মা পিঠা বানাতেন। সেই ধোঁয়া ওঠা পিঠার গন্ধ, নারিকেলের মিষ্টি
              স্বাদ — এগুলো আমার শৈশবের সেরা স্মৃতি। আর আমাদের বাগানের গাছ থেকে পেড়ে আনা তাজা ফলের জুস।
              সেই স্বাদ আর সেই বিশুদ্ধতাকেই আমি নির্ঝরণের মাধ্যমে সখিপুরের মানুষের কাছে পৌঁছে দিতে চাই।
            </p>
            <p className="text-forest font-semibold mt-4 bn">— নির্ঝরণের প্রতিষ্ঠাতা</p>
          </div>

          <p className="text-gray-600 text-base leading-relaxed bn mb-6">
            ২০২২ সালে গার্লস স্কুল রোডে একটি ছোট্ট স্টল থেকে যাত্রা শুরু হয়েছিল নির্ঝরণের।
            প্রতিদিন সকালে তাজা ফল কিনে এনে জুস বানানো, কাস্টমারদের মুখে হাসি দেখা — এটাই ছিল
            আমাদের সবচেয়ে বড় পুরস্কার।
          </p>
          <p className="text-gray-600 text-base leading-relaxed bn mb-6">
            আস্তে আস্তে মানুষ জানতে পারল যে এখানে কোনো কেমিক্যাল নেই, কোনো ভেজাল নেই।
            শুধু আছে প্রকৃতির দান আর পরিশ্রমের ভালোবাসা। তখন থেকেই নির্ঝরণ হয়ে উঠল
            সখিপুরের মানুষের বিশ্বস্ত বন্ধু।
          </p>
          <p className="text-gray-600 text-base leading-relaxed bn">
            ২০২৪ সালে আমরা আমাদের স্থায়ী শপ খুলেছি। এখন শুধু জুস নয়, ঐতিহ্যবাহী পিঠার স্বাদও
            নিতে পারছেন একই ছাদের নিচে। ভবিষ্যতে আমরা সখিপুরের প্রতিটি বাড়িতে নির্ঝরণের সতেজতা
            পৌঁছে দিতে চাই।
          </p>
        </div>
      </section>

      {/* Values */}
      <section className="bg-cream-dark py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-10">
            <h2 className="section-title">আমাদের মূল্যবোধ</h2>
            <p className="section-subtitle bn">যে নীতিগুলো আমাদের প্রতিটি কাজকে পরিচালিত করে</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {values.map((v) => {
              const Icon = v.icon
              return (
                <div key={v.title} className="bg-white rounded-2xl p-6 shadow-brand hover:shadow-brand-lg transition-shadow flex gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${v.color.split(' ')[0]}`}>
                    <Icon className={`w-6 h-6 ${v.color.split(' ')[1]}`} />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg mb-2 bn">{v.title}</h3>
                    <p className="text-gray-600 text-sm leading-relaxed bn">{v.desc}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 py-16">
        <div className="text-center mb-10">
          <h2 className="section-title">আমাদের যাত্রাপথ</h2>
          <p className="section-subtitle bn">ছোট্ট স্বপ্ন থেকে বড় পরিবর্তনের গল্প</p>
        </div>
        <div className="relative">
          <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-0.5 bg-forest/20 -translate-x-1/2" />
          <div className="space-y-8">
            {milestones.map((m, i) => (
              <div
                key={m.year}
                className={`relative flex items-start gap-6 ${i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}
              >
                {/* Dot */}
                <div className="absolute left-8 md:left-1/2 -translate-x-1/2 w-4 h-4 bg-orange-brand rounded-full border-4 border-cream shadow-orange z-10" />

                {/* Content */}
                <div className={`ml-16 md:ml-0 md:w-5/12 bg-white rounded-2xl p-6 shadow-brand ${i % 2 === 0 ? 'md:mr-auto' : 'md:ml-auto'}`}>
                  <span className="text-orange-brand font-bold text-lg bn">{m.year}</span>
                  <h3 className="font-bold text-gray-900 text-base mt-1 bn">{m.title}</h3>
                  <p className="text-gray-600 text-sm mt-2 leading-relaxed bn">{m.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Roadmap */}
      <section
        className="py-16 px-4"
        style={{ background: 'linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)' }}
      >
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-cream mb-3 bn" style={{ fontFamily: 'Hind Siliguri, sans-serif' }}>
            ভবিষ্যৎ পরিকল্পনা
          </h2>
          <p className="text-cream/70 mb-10 bn">আমরা যেখানে যেতে চাই</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
            {[
              { emoji: '🌐', title: 'nirjharon.com লঞ্চ', desc: 'পূর্ণাঙ্গ অনলাইন প্ল্যাটফর্ম।' },
              { emoji: '🛵', title: 'দ্রুত ডেলিভারি', desc: 'সখিপুরে ১৫-২০ মিনিটে ডেলিভারি।' },
              { emoji: '📅', title: 'সাবস্ক্রিপশন প্ল্যান', desc: 'নিয়মিত জুসের মাসিক প্যাকেজ।' },
              { emoji: '🤝', title: 'ইনফ্লুয়েন্সার কোলাব', desc: 'সখিপুরের মুখগুলোর সাথে কাজ।' },
            ].map((item) => (
              <div key={item.title} className="bg-white/10 backdrop-blur-sm rounded-2xl p-5 border border-white/20">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-2xl">{item.emoji}</span>
                  <h4 className="font-bold text-cream bn">{item.title}</h4>
                </div>
                <p className="text-cream/60 text-sm bn">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
