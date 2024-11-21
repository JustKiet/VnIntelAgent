'use client'
import { 
    Box, 
    Typography, 
    Dialog,
    DialogContentText
} from "@mui/material";
import LinearProgressWithLabel from './LinearProgressWithLabel';

interface LoadingDialogProps {
    open: boolean;
    stage: string;
    progress: number;
}

export default function LoadingDialog({ open, stage, progress }: LoadingDialogProps) {
    return (
        <Box>
            <Dialog maxWidth="md" fullWidth={true} open={open}>
                <Box sx={{ display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'center'}}>
                        <DialogContentText sx={{ marginY: 3 }}>
                            <Typography variant="h6" color="black" gutterBottom>
                                {stage}
                            </Typography>
                        </DialogContentText>
                    </Box>
                    <LinearProgressWithLabel value={progress} />
                    <Box sx={{ display: 'flex', justifyContent: 'center'}}>
                        <DialogContentText sx={{ marginY: 1 }}>
                            <Typography color="info" sx={{ fontStyle: 'italic', fontWeight: 300 }} gutterBottom>
                                **Quá trình này có thể mất vài phút. Vui lòng không thoát khỏi trang!
                            </Typography>
                        </DialogContentText>
                    </Box>
                </Box>
            </Dialog>
        </Box>
    );
}
