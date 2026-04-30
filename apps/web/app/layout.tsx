import type { Metadata } from 'next';
import '../src/styles/globals.css';

export const metadata: Metadata = {
  title: 'JARVIS OS',
  description: 'Personal AI Operating System',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0A0E14] text-white font-sans antialiased">{children}</body>
    </html>
  );
}
