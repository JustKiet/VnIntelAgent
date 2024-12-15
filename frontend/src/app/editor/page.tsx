'use client'

import '@mdxeditor/editor/style.css'
import { ForwardRefEditor } from '../components/ForwardRefEditor';
import { Box, Chip, Tooltip } from '@mui/material';
import { useEffect, useState } from 'react';
import { createTheme, responsiveFontSizes, ThemeProvider } from '@mui/material/styles';
import Typography from "@mui/material/Typography";
import Divider from '@mui/material/Divider';
import { useSearchParams } from 'next/navigation';
import React from 'react';
import { MDXEditorMethods } from '@mdxeditor/editor';
import { marked } from 'marked';
import Button from '@mui/material/Button';
import Textarea from '@mui/joy/Textarea';

let theme = createTheme();
theme = responsiveFontSizes(theme);

function ArticleEditor() {
    const ref = React.useRef<MDXEditorMethods>(null)
    const searchParams = useSearchParams();
    const task_id = searchParams.get('task_id');
    const [wordCount, setWordCount] = useState(0);
    const [content, setContent] = useState('');
    const [description, setDescription] = useState('');
    const [keywords, setKeywords] = useState([]);
    const [copiedText, setCopiedText] = useState('');
    const [openTooltip, setOpenTooltip] = useState(false);

    const handleCopy = (keyword: string) => () => {
        navigator.clipboard.writeText(keyword);
        setCopiedText(keyword);
        setOpenTooltip(true);
        setTimeout(() => setOpenTooltip(false), 1000);
    };

    const handleTextChange = (e: string) => {
        setContent(e);
        const words = e.trim().split(/\s+/);
        setWordCount(words.filter(word => word).length);
    };

    const handleCopyAsHTML = () => {
        const html = marked(content);
        try {
            navigator.clipboard.writeText(html);
        } catch (error) {
            console.error("Error converting markdown to HTML:", error);
        }
    };

    useEffect(() => {
        if (task_id) {
            // Fetch the full article once
            const fetchArticle = async () => {
                try {
                    const response = await fetch(`http://localhost:8000/get-seo-content?task_id=${task_id}`);
                    const data = await response.json()
                    console.log(data);
                    const article = data.article
                    const description = data.description
                    const keywords = data.keywords["keywords"]
                    setKeywords(keywords)

                    console.log(description);
                    setDescription(description);
                    setContent(article);
                    ref.current?.setMarkdown(article);
                    handleTextChange(article);
                } catch (error) {
                    console.error("Error fetching article:", error);
                }
            };
    
            fetchArticle();
        }
    }, [task_id]);

    return (
        <main style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%', backgroundColor: '#F4F4F6' }}>
            <Box sx={{ width: '100%', height: '100%'}}>
                <Box component="section" sx={{ display: 'flex', flexDirection: 'row', width: '100%', minHeight: '100vh', height: '100%' }}>
                    <Box sx={{ display: 'flex', flexDirection: 'row', width: '78%' }}>
                        <ForwardRefEditor
                            ref={ref}
                            markdown={ content }
                            onChange={ handleTextChange }
                            className='w-full bg-neutral-100 h-full whitespace-pre-wrap'
                        />
                        <Box sx={{ display: 'flex', flexDirection: 'column', width: '20%', top: '0', right: '0', height: '100vh', backgroundColor: '#FFFFFF', position: 'fixed', borderRadius: '0.375rem'  }}>
                            <Box sx={{ display: 'flex', height: '7%', width: '100%', alignItems: 'center', justifyContent: 'center' }}>
                                <Box sx={{ display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'center' }}>
                                    <ThemeProvider theme={theme}>
                                        <Typography variant='h6' style={{ fontWeight: 800 }}>
                                            Tổng số từ
                                        </Typography>
                                    </ThemeProvider>
                                </Box>
                                <Divider orientation='vertical' variant='middle' flexItem />
                                <Box sx={{ display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'center'}}>
                                    <ThemeProvider theme={theme}>
                                        <Typography variant='h6' style={{ fontWeight: 400, color: '' }}>
                                            { wordCount }
                                        </Typography>
                                    </ThemeProvider>
                                </Box>
                            </Box>
                            <Divider variant='middle' flexItem/>
                            <Box sx={{ display: 'flex', height: '200px', width: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
                                <Box sx={{ display: 'flex', height: '100%', width: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
                                    <Box sx={{ display: 'flex', width: '90%', alignItems: 'center', justifyContent: 'start'}}>
                                        <ThemeProvider theme={theme}>
                                            <Typography variant='h6' style={{ fontWeight: 600, color: '' }}>
                                                Mô tả:
                                            </Typography>
                                        </ThemeProvider>
                                    </Box>
                                    <Textarea
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        size='sm'
                                        minRows={4}
                                        maxRows={4}
                                        sx={{ width: '90%', height: '70%', margin: '5px' }}
                                    />
                                </Box>
                            </Box>
                            <Box sx={{ display: 'flex', height: '400px', width: '100%', alignItems: 'center', justifyContent: 'start', flexDirection: 'column' }}>
                                <Box sx={{ display: 'flex', width: '90%', alignItems: 'center', justifyContent: 'start'}}>
                                    <ThemeProvider theme={theme}>
                                        <Typography variant='h6' style={{ fontWeight: 800 }} gutterBottom>
                                            Từ khóa liên quan:
                                        </Typography>
                                    </ThemeProvider>
                                </Box>
                                <Box
                                    sx={{
                                        display: "flex",
                                        flexWrap: "wrap",
                                        gap: 1,
                                        maxHeight: "380px",  // Set max height
                                        overflowY: "auto",  // Enable scrolling if content overflows
                                        p: 2,
                                        bgcolor: "background.paper",
                                        borderRadius: 2,

                                        // Custom Scrollbar styles
                                        "&::-webkit-scrollbar": {
                                        width: "8px",  // Width of the scrollbar
                                        },
                                        "&::-webkit-scrollbar-thumb": {
                                        backgroundColor: "#888",  // Color of the scrollbar thumb
                                        borderRadius: "10px",  // Round the edges of the thumb
                                        "&:hover": {
                                            backgroundColor: "#555",  // Hover color of the thumb
                                        },
                                        },
                                        "&::-webkit-scrollbar-track": {
                                        backgroundColor: "#f1f1f1",  // Color of the scrollbar track
                                        borderRadius: "10px",  // Round the edges of the track
                                        },
                                    }}
                                    >
                                    {keywords.map((keyword: string, index: number) => (
                                        <Tooltip title='Copied to Clipboard!' placement='top' open={openTooltip && copiedText === keyword} key={index} arrow>
                                            <Chip key={index} label={keyword} onClick={handleCopy(keyword)}/>
                                        </Tooltip>
                                    ))}
                                </Box>
                            </Box>
                            <Box sx={{ display: 'flex', height: '10%', width: '100%', alignItems: 'center', justifyContent: 'center' }}>
                                <Button variant='contained' onClick={ handleCopyAsHTML } sx={{ width: '90%' }}>
                                    Copy as HTML
                                </Button>
                            </Box>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </main>
    )
}

export default ArticleEditor