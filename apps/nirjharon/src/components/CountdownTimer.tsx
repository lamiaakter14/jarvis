import { useState, useEffect } from 'react'
import { Clock } from 'lucide-react'

interface CountdownTimerProps {
  targetTime?: string // e.g. "22:00" (10 PM today)
  label?: string
}

function getSecondsUntil(timeStr: string): number {
  const now = new Date()
  const [h, m] = timeStr.split(':').map(Number)
  const target = new Date(now)
  target.setHours(h, m, 0, 0)
  if (target <= now) target.setDate(target.getDate() + 1)
  return Math.floor((target.getTime() - now.getTime()) / 1000)
}

export default function CountdownTimer({
  targetTime = '22:00',
  label = 'এই অফার শেষ হতে বাকি',
}: CountdownTimerProps) {
  const [secs, setSecs] = useState(() => getSecondsUntil(targetTime))

  useEffect(() => {
    const timer = setInterval(() => {
      setSecs((prev) => {
        if (prev <= 1) return getSecondsUntil(targetTime)
        return prev - 1
      })
    }, 1000)
    return () => clearInterval(timer)
  }, [targetTime])

  const hours = Math.floor(secs / 3600)
  const minutes = Math.floor((secs % 3600) / 60)
  const seconds = secs % 60

  const pad = (n: number) => String(n).padStart(2, '0')

  return (
    <div className="inline-flex flex-col items-center gap-2">
      <div className="flex items-center gap-1.5 text-white/80 text-sm">
        <Clock className="w-4 h-4" />
        <span className="bn">{label}</span>
      </div>
      <div className="flex gap-2">
        {[
          { value: pad(hours), label: 'ঘণ্টা' },
          { value: pad(minutes), label: 'মিনিট' },
          { value: pad(seconds), label: 'সেকেন্ড' },
        ].map((unit, i) => (
          <div key={i} className="flex flex-col items-center">
            <div className="bg-white/20 backdrop-blur-sm rounded-xl w-14 h-14 flex items-center justify-center">
              <span className="text-2xl font-bold text-white tabular-nums" style={{ fontFamily: 'Lato, sans-serif' }}>
                {unit.value}
              </span>
            </div>
            <span className="text-white/60 text-xs mt-1 bn">{unit.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
