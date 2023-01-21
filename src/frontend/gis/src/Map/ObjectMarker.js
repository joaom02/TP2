import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties
    const {id, imgUrl, name} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgUrl,
                iconRetinaUrl: imgUrl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl}/>
                        </ListItemIcon>
                        <ListItemText primary={name}/>
                    </ListItem>
                </List>

            </Popup>
        </Marker>
    )
}