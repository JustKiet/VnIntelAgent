'use client';
import * as React from 'react';
import { 
    useState,
} from 'react';
import { 
    Box, 
    Button, 
    Typography,
    ToggleButton,
    ToggleButtonGroup,
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { useRouter } from 'next/navigation';
import LoadingDialog from './LoadingDialog';

export default function WriterForm() {
    const [agentName, setAgentName] = useState('');
    const [keyword, setKeyword] = useState('');
    const [model, setModelChoice] = useState('gpt-4o-mini');
    const [articleTone, setArticleTone] = useState('professional');
    const [language, setLanguage] = useState('vietnamese');
    const [wordCount, setWordCount] = useState(500);
    const [additionalPrompt, setAdditionalPrompt] = useState('');
    const [submitText, setSubmitText] = useState('Tạo bài viết');

    const [open, setOpen] = useState(false);
    const [stage, setStage] = useState('Đang tải...')
    const [progress, setProgress] = useState(0)

    const nodeValue = {
        "initialize": "Đang tạo khung ban đầu...",
        "research": "Đang tìm kiếm thông tin...",
        "retrieval": "Đang tạo embedding...",
        "refine": "Đang tinh chỉnh khung bài viết...",
        "get_keywords": "Đang lấy từ khóa liên quan...",
        "write_description": "Đang viết mô tả...",
        "write_sections": "Đang viết từng mục...",
        "write_article": "Đang tạo bài viết hoàn chỉnh...",
    }

    const router = useRouter();

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleArticleChange = (event: any, newArticleTone: React.SetStateAction<string> | null) => {
        if (newArticleTone !== null) {
          setArticleTone(newArticleTone);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitText('Đang tạo bài viết...');
        if (!router) return;

        setOpen(true)

        console.log(agentName, keyword, model, articleTone, wordCount, additionalPrompt);

        const formData = {
            user_id: "1",
            agent_name: agentName,
            keyword: keyword,
            language: language,
            article_tone: articleTone,
            model: model,
            word_count: wordCount,
            additional_prompt: additionalPrompt
        }

        const response = await fetch('http://localhost:8000/generate-seo-content/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })

        const data = await response.json();

        if (response.ok) {
            if (data && data.task_id) {
                const { task_id } = data;
                const eventSource = new EventSource(`http://localhost:8000/stream-seo-content?task_id=${task_id}`);

                eventSource.onmessage = (event) => {

                    const data = event.data;
                
                    const parsedData: { 
                        node?: keyof typeof nodeValue, 
                        progress?: number ,
                    } = JSON.parse(data);

                    if (parsedData.node) {
                        console.log(parsedData.node);
                        const mappedNode = nodeValue[parsedData.node] || "Unknown";
                        setStage(mappedNode);
                    }

                    if (parsedData.progress) {
                        console.log(parsedData.progress);
                        setProgress(Number(parsedData.progress));
                    }
                };

                eventSource.onerror = () => {
                    eventSource.close();
                    router.push(`/editor?task_id=${task_id}`);
                }

            } else {
                console.error('task_id not found in the response');
            }
        } else {
            console.log('Error submitting form', data);
        }

        
    };

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: "100%", height: "100vh" }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '90%', width: '100%' }}>
                <Box component="form" sx={{ display: 'flex', width: '620px', justifyContent: 'start', flexDirection: 'column' }}>
                    <Box sx={{ display: 'flex', width: '100%', justifyContent: 'start', flexDirection: 'column', paddingBottom: '10px' }}>
                        <Box sx={{ display: 'flex', justifyContent: 'start' }}>
                            <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                Tên cuộc trò chuyện:
                            </Typography>
                        </Box>
                        <FormControl required={true}>
                            <TextField onChange={(e) => setAgentName(e.target.value)} value={agentName} id='agentName' placeholder='VD: Viết báo Nghiên cứu' variant="outlined" sx={{ width: '100%' }}></TextField>
                        </FormControl>
                    </Box>
                    <Box sx={{ display: 'flex', width: '100%', justifyContent: 'start', flexDirection: 'column', paddingBottom: '10px' }}>
                        <Box sx={{ display: 'flex', justifyContent: 'start', flexDirection: 'column'}}>
                            <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                Từ khóa:
                            </Typography>
                            <FormControl required>
                                <TextField onChange={(e) => setKeyword(e.target.value)} value={keyword} id='agentName' placeholder='VD: Tác nhân AI là gì?' variant="outlined" sx={{ width: '100%' }}></TextField>
                            </FormControl>
                        </Box>
                    </Box>
                    <Grid container sx={{ width: '100%', justifyContent: 'space-between' }}>
                        <Grid size={{ xs: 10, lg: 8 }} sx={{ paddingBottom: '10px', width: '100%' }}>
                            <Box sx={{ display: 'flex', justifyContent: 'start' }}>
                                <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                    Giọng điệu của bài viết:
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', width: '100%', justifyContent: 'center', alignItems: 'center', paddingY: '5px'}}>
                                <FormControl sx={{ width: '100%' }} required>
                                    <ToggleButtonGroup sx={{ width: '100%' }} color='primary' value={articleTone} onChange={handleArticleChange} exclusive>
                                        <ToggleButton value="normal">
                                            Thông thường
                                        </ToggleButton>
                                        <ToggleButton value="blogpost">
                                            Blogpost
                                        </ToggleButton>
                                        <ToggleButton value="professional">
                                            Chuyên nghiệp
                                        </ToggleButton>
                                    </ToggleButtonGroup>
                                </FormControl>
                            </Box>
                        </Grid>
                        <Grid size={{ xs: 10, lg: 4 }} sx={{ paddingBottom: '10px', width: '100%' }}>
                            <Box sx={{ display: 'flex', justifyContent: 'start' }}>
                                <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                    Ngôn ngữ
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', width: '100%', paddingY: '5px'}}>
                                <FormControl sx={{ width: '100%' }} required>
                                    <Select labelId='language' id='language-select' value={language} onChange={(e) => setLanguage(e.target.value)}>
                                        <MenuItem value={'vietnamese'}>Tiếng Việt</MenuItem>
                                        <MenuItem value={'english'}>English</MenuItem>
                                    </Select>
                                </FormControl>
                            </Box>
                        </Grid>
                    </Grid>
                    <Grid container spacing={0} sx={{ width: '100%', justifyContent: 'space-between' }}>
                        <Grid size={{ xs: 10, lg: 8 }} sx={{ paddingBottom: '10px', width: '100%' }}>
                            <Box sx={{ display: 'flex', width: '100%', justifyContent: 'start', alignItems: 'center'}}>
                                <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                    Chọn mô hình:
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', width: '80%'}}>
                                <FormControl sx={{ width: '100%' }} required>
                                    <Select labelId='model' id='model-select' value={model} onChange={(e) => setModelChoice(e.target.value)}>
                                        <MenuItem value={'gpt-4o-mini'}>gpt-4o-mini</MenuItem>
                                        <MenuItem value={'gpt-4o'}>gpt-4o</MenuItem>
                                    </Select>
                                </FormControl>
                            </Box>
                        </Grid>
                        <Grid size={{ xs: 10, lg: 4 }} sx={{ paddingBottom: '10px', width: '100%' }}>
                            <Box sx={{ display: 'flex', width: '100%', justifyContent: 'start', alignItems: 'center' }}>
                                <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                    Số từ:
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', width: '100%'}}>
                                <FormControl required>
                                    <TextField type='number' value={wordCount} onChange={(e) => setWordCount(Number(e.target.value))} id='numWords' placeholder='VD: 1000' variant='outlined' sx={{ width: '100%' }}></TextField>                                    
                                </FormControl>
                            </Box>
                        </Grid>
                    </Grid>
                    <Box sx={{  display: 'flex', width: '100%', flexDirection: 'column', justifyContent: 'start', alignItem: 'center'}}>
                        <Box sx={{ display: 'flex', justifyContent: 'start'}}>
                            <Typography variant='subtitle1' sx={{ fontWeight: 300 }} gutterBottom>
                                Viết Prompt chỉ dẫn:
                            </Typography>
                        </Box>
                        <FormControl>
                            <TextField value={additionalPrompt} onChange={(e) => setAdditionalPrompt(e.target.value)} id='prompt' multiline={true} rows={4} placeholder='VD: Viết một bài về tác nhân AI' variant='outlined' sx={{ width: '100%' }}></TextField>
                        </FormControl>
                    </Box>
                    <Box sx={{ display: 'flex', width: '100%', flexDirection: 'column', justifyContent: 'start', alignItem: 'center'}}>
                        <Button variant='contained' onClick={handleSubmit} sx={{ width: '100%', marginTop: '10px' }}>
                            {submitText}
                        </Button>
                    </Box>
                    <LoadingDialog open={open} stage={stage} progress={progress}/>
                </Box>
            </Box>
        </Box>
    )
}