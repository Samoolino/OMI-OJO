import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OMI-OJO | Climate & Environmental Data",
  description: "Climate, environmental data, evidence, dMRV and institutional reporting infrastructure.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><div style={{position:"sticky",top:0,zIndex:1000,padding:"8px 16px",display:"flex",gap:16,justifyContent:"center",alignItems:"center",background:"rgba(5,24,25,.96)",borderBottom:"1px solid rgba(120,190,160,.18)",fontSize:12,letterSpacing:".08em"}}><a href="/lagos-to-dubai" style={{textDecoration:"none"}}>LAGOS → DUBAI · GLOBAL PILOT</a><span style={{opacity:.35}}>·</span><a href="/reporting" style={{textDecoration:"none",color:"#9ee8cd"}}>REPORTING READ MODEL</a></div>{children}</body></html>;
}
