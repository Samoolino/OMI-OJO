import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Blue-Ether OS | Water Intelligence & DMRV",
  description: "Investor-grade rainwater intelligence, provenance, DMRV and ESG evidence platform.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
