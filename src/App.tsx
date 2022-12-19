import { useState, useEffect } from 'react';
import './App.css';
import { MediaItemInfo, ShortTrackInfo } from './interfaces/projectinfo';
import { socket } from './hooks/context';
import { TopBanner } from './components/TopCarousel';
import { MutedSoloTracklist } from './components/MutedSoloTracklist';

function App() {
    const [ projectTitle, setProjectTitle ] = useState("No project open.");
    const [ selectedItemInfo, setSelectedItemInfo ] = useState<MediaItemInfo>();
    const [ solodTracks, setSolodTracks ] = useState<ShortTrackInfo[]>([]);
    const [ mutedTracks, setMutedTracks ] = useState<ShortTrackInfo[]>([]);

    useEffect(() => {
        socket.on("project-name-change", (newTitle: string) => {
            setProjectTitle(newTitle);
        });

        socket.on("project-selection-change", (selecteditem?: MediaItemInfo) => {
            setSelectedItemInfo(selecteditem);
            console.log(selecteditem);

            if (window.obsstudio) {
                window.obsstudio.setCurrentScene(
                    selecteditem ? "Pianoroll Screen" : "Reaper Timeline"
                );
            }
        });

        socket.on("project-solod-channels-change", (solodItems: ShortTrackInfo[]) => {
            setSolodTracks(solodItems);
        });

        socket.on("project-muted-channels-change", (mutedItems: ShortTrackInfo[]) => {
            setMutedTracks(mutedItems);
        });
    }, []);

    return (
        <div className="App" style={{width: "100vw", height: "100vh"}}>
            <TopBanner projectTitle={projectTitle} selectedItemInfo={selectedItemInfo} />
            <MutedSoloTracklist mutedTracks={mutedTracks} solodTracks={solodTracks} />
        </div>
    );
}

export default App;
