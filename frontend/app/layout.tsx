import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Blue-Ether OS | Investment & dMRV Intelligence',
  description: 'Institutional evidence interface for rainwater, environmental data, DMRV and sustainable infrastructure.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
