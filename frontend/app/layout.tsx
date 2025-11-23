import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import { Toaster } from "@/app/components/ui/sonner";
import "./globals.css";

const nunito = Nunito({
  weight: ['300', '400', '600', '700', '800', '900'],
  subsets: ["latin"],
  variable: "--font-nunito",
});

export const metadata: Metadata = {
  title: "HealthForAll",
  description: "Encuentra doctores, clínicas y especialidades médicas en Perú",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${nunito.variable} font-sans antialiased`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
