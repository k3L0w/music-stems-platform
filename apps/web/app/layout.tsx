import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Music Stems Platform",
  description: "MVP web conectado a API da plataforma de separacao musical."
};

type RootLayoutProps = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
