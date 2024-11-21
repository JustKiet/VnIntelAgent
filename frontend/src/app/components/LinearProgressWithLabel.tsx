'use client'
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import LinearProgress, { linearProgressClasses, LinearProgressProps } from '@mui/material/LinearProgress';
import { grey } from '@mui/material/colors';

export default function LinearProgressWithLabel(props: LinearProgressProps & { value: number }) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Box sx={{ width: '90%', mr: 1, marginY: 3 }}>
          <LinearProgress variant="determinate" color='primary' sx={{ height: 5, [`&.${linearProgressClasses.bar}`]: {borderRadius: 3, backgroundColor: '#1a90ff'}, [`&.${linearProgressClasses.colorPrimary}`]: {backgroundColor: grey[200]} }} {...props} />
        </Box>
        <Box sx={{ minWidth: 35 }}>
          <Typography
            variant="body2"
            sx={{ color: 'text.secondary' }}
          >{`${Math.round(props.value)}%`}</Typography>
        </Box>
      </Box>
    );
}
