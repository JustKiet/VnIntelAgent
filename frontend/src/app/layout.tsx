import type { Metadata } from "next";
import "./globals.css";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter';
import { Roboto } from "next/font/google";
import Sidebar from "./components/Sidebar";
import Box from "@mui/system/Box";

export const metadata: Metadata = {
  title: "SEO Agent",
  description: "Công cụ viết bài SEO sử dụng công nghệ đa tác nhân LLM tân tiến nhất.",
};

const roboto = Roboto({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto',
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={roboto.variable}>
        <AppRouterCacheProvider>
          <Box sx={{ display: 'flex', flexDirection: 'row' }}>
            <Sidebar></Sidebar>
            {children}
          </Box>
        </AppRouterCacheProvider>    
      </body>
    </html>
  );
}
