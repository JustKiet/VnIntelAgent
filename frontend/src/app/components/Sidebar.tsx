'use client'
import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import PermIdentityOutlinedIcon from '@mui/icons-material/PermIdentityOutlined';
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import LibraryBooksOutlinedIcon from '@mui/icons-material/LibraryBooksOutlined';
import SsidChartOutlinedIcon from '@mui/icons-material/SsidChartOutlined';
import BoltOutlinedIcon from '@mui/icons-material/BoltOutlined';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import Zoom from '@mui/material/Zoom';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import grey from '@mui/material/colors/grey';

const drawerWidth = 90;

const iconStyle = {
  fontSize: 35,
  color: grey[800],
};

const listItemStyle = {
  display: 'flex',
  justifyContent: 'center',
};

const buttonStyle = {
  maxWidth: '70px',
  maxHeight: '70px',
  minWidth: '70px',
  minHeight: '70px',
  borderRadius: '20px',
  color: grey[600],
  backgroundColor: grey[100],
  '&:hover': {
    backgroundColor: grey[200],
  },
}

export default function Sidebar() {

  const handleHomeRedirect = () => {
    window.location.href = '/';
  }

  return (
    <Drawer sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: drawerWidth, flexShrink: 0, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' } }} variant="permanent" anchor="left">
      <List sx={{display: 'flex', justifyContent: 'center', flexDirection: 'column', height: "100%"}}>
        <Divider />
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Trang chủ" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle } onClick={handleHomeRedirect}>
              <HomeOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem> 
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Tổng quan" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <DashboardOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Hồ sơ" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <PermIdentityOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Viết bài" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <CreateOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Bài Blogs" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <LibraryBooksOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Thống kê" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <SsidChartOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider variant='middle'/>
        <ListItem style={ listItemStyle }>
          <Tooltip slotProps={{ tooltip: {sx: {backgroundColor: grey[800], fontSize: 20 }}}} title="Thanh toán" placement='right' TransitionComponent={Zoom} leaveDelay={200}>
            <Button sx={ buttonStyle }>
              <BoltOutlinedIcon style={ iconStyle }/>
            </Button>
          </Tooltip>
        </ListItem>
        <Divider />
      </List>
    </Drawer>
  )
}