import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Meu Pedaço Favorito",
  description: "SaaS para pizzarias de venda por pedaço",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
