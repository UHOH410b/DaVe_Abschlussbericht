import "./globals.css";

export const metadata = {
  title: "Agrardatenkatalog BW",
  description: "Suche in atomaren Anforderungen aus Agrarrecht, Standards und Richtlinien."
};

export default function RootLayout({ children }) {
  return (
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}
