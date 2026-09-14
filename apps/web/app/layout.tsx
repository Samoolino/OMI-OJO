import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Blue-Ether OS | Water Intelligence & DMRV",
  description: "Investor-grade rainwater intelligence, provenance, DMRV and ESG evidence platform.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><div style={{position:"sticky",top:0,zIndex:1000,padding:"8px 16px",textAlign:"center",background:"rgba(5,24,25,.94)",borderBottom:"1px solid rgba(120,190,160,.18)"}}><a href="/lagos-to-dubai" style={{textDecoration:"none",fontSize:12,letterSpacing:".08em"}}>LAGOS → DUBAI · GLOBAL PREMIUM RAINWATER + ESG EVIDENCE PILOT</a></div>{children}</body></html>;
}
