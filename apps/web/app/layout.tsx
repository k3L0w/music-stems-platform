import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Music Stems Platform",
  description: "Scaffolding inicial da plataforma de separacao musical."
};

type RootLayoutProps = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
