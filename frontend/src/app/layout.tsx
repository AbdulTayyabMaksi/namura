import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import { Providers } from "@/components/providers/Providers";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ArthSaathi 2.0 — AI Financial Digital Twin",
  description:
    "Multi-agent Agentic AI system creating a living Financial Digital Twin for every Indian citizen. Nomura KakushIN 10.0.",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#0a0f1c",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
