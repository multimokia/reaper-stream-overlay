import React from 'react';
import { useState, useEffect } from 'react';
import { Carousel } from 'react-bootstrap';
import './App.css';
import { useFetch } from './hooks/useFetch'
import { ProjectInfo } from './interfaces/projectinfo';
import * as Icon from 'react-bootstrap-icons';

function App() {
    const { data, refetch } = useFetch<ProjectInfo>("http://localhost:8000/api/reaper/projectinfo");
    const [refreshInterval, setRefreshInterval] = useState(1000);

    useEffect(() => {
        if (refreshInterval && refreshInterval > 0) {
            const interval = setInterval(refetch, refreshInterval);
            return () => clearInterval(interval);
        }
    });

    const [r, g, b] = data.selected_media_items.length === 0 ? [33, 33, 33] : data.selected_media_items[0].track_color;
    return (
        <div className="App" style={{width: "100vw", height: "100vh"}}>
            <Carousel
                controls={false}
                fade={true}
                interval={10000}
                indicators={false}
                style={{
                    background: "#343434",
                    height: 50,
                    bottom: "0px",
                    color: "white",
                    fontFamily: "Poppins",
                    fontWeight: "bolder"
                }}
            >
                <Carousel.Item
                >
                    <h1>{data.project_name === "" ? "No project open" : `Project: ${data.project_name}`}</h1>
                </Carousel.Item>
                <Carousel.Item
                    style={{
                        background: `rgb(${r}, ${g}, ${b})`
                    }}
                >
                    <h1>{data.selected_media_items.length === 0 ? "No item selected" : `Editing ${data.selected_media_items[0].track_name} | ${new Date(data.selected_media_items[0].start_time * 1000).toISOString().substring(14, 19)} - ${new Date(data.selected_media_items[0].end_time * 1000).toISOString().substring(14, 19)}`}</h1>
                </Carousel.Item>
                <Carousel.Item
                >
                    <h1><table width={"100%"}><td><Icon.Twitter/> @multimokia</td><td><Icon.Youtube/> Subscribe!</td></table></h1>
                </Carousel.Item>
            </Carousel>
        </div>
    );
}

export default App;
