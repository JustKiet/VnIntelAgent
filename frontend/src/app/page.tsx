'use client';
import Box from "@mui/system/Box";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";
import { TypeAnimation } from 'react-type-animation';
import { grey } from "@mui/material/colors";
import Grid from "@mui/material/Grid2";
import { createTheme, responsiveFontSizes, ThemeProvider } from '@mui/material/styles';
import WriterForm from "./components/WriterForm";
import { OpenAIIcon } from "./components/media/LogoIcons";
import { GoogleIcon } from "./components/media/LogoIcons";
import { LangchainIcon } from "./components/media/LogoIcons";

let theme = createTheme();
theme = responsiveFontSizes(theme);

export default function Home() {
  return (
    <main className="Home" style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%'}}>
      <Box component="section" sx={{ height: { md: '200vh', lg: '100vh' }, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ height: "100%", width: "100%" }}>
          <Grid container spacing={2} sx={{ height: "100%" }}>
            <Grid size={{ xs:12, lg: 6  }} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minheight: "100%"}}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: "50%", height: "100vh" }}>
                <Grid container spacing={1} sx={{ justifyContent: 'center', alignItems: 'center', height: '90%' }}>
                  <Grid size={12}>
                    <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                      <Box sx={{ width: 80, height: 30, border: 1, bgcolor: 'transparent', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <ThemeProvider theme={theme}>
                          <Typography variant="h6" style={{ fontWeight: 300 }}>
                            Demo
                          </Typography>
                        </ThemeProvider>
                      </Box>
                      <br />
                      <ThemeProvider theme={theme}>
                        <Typography variant="h1" gutterBottom>
                          SEO Agent:
                        </Typography>
                      </ThemeProvider>
                      <Box sx={{ width: "620px", display: 'block' }}>
                        <TypeAnimation
                            sequence={[
                              'Viết bài trong nháy mắt.',
                              2000,
                              'Luôn cập nhật thông tin.',
                              2000,
                              'Tối ưu hóa SEO.',
                              2000,
                              'Cải thiện SERP.',
                              2000,
                            ]}
                            speed={50}
                            style={{ 
                              fontSize: '3.5em',
                              color: grey[800],
                              fontFamily: 'Roboto',
                              fontWeight: 300,
                            }}
                            repeat={Infinity}
                            preRenderFirstString={true}
                          />
                      </Box>
                      <Box sx={{ display: 'flex', height: '100%', paddingY: '20px', alignItems: 'center'}}>
                        <ThemeProvider theme={theme}>
                          <Typography sx={{ fontWeight: 300, fontStyle: 'italic' }} variant="h6" gutterBottom>
                            Công cụ viết bài SEO sử dụng công nghệ đa tác nhân LLM tân tiến nhất.
                          </Typography>
                        </ThemeProvider>
                      </Box>
                    </Box>
                  </Grid>
                  <Grid size={12}>
                    <Box sx={{ paddingTop: '60px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '620px'}}>
                      <Box sx={{ display: 'flex', width: '100%', flexDirection: 'column'}}>
                        <Box sx={{ display: 'flex', justifyContent: 'start'}}>
                          <ThemeProvider theme={theme}>
                            <Typography variant="h6" sx={{ fontWeight: 300 }} gutterBottom>
                              Powered By:
                            </Typography>
                          </ThemeProvider>
                        </Box>
                        <Box sx={{ display: 'flex', width: '100%', height: '100%'}}>
                          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingRight: 5 }}>
                            <OpenAIIcon sx={{ fontSize: 170}}/>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingRight: 5 }}>
                            <GoogleIcon sx={{ fontSize: 170}}/>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingRight: 5 }}>
                            <LangchainIcon sx={{ fontSize: 170}}/>
                          </Box>
                        </Box>
                      </Box>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
            <Grid size={{ xs: 12, lg: 6 }} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minheight: "100%"}}>
              <WriterForm></WriterForm>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </main>
  );
}
