import { ShortTrackInfo } from "../interfaces/projectinfo";
import { TrackList } from "./Tracklist";

export const MutedSoloTracklist: React.FC<{mutedTracks: ShortTrackInfo[], solodTracks: ShortTrackInfo[]}> = ({mutedTracks, solodTracks}) => {
    if (mutedTracks.length === 0 && solodTracks.length === 0) {
        return (<></>);
    }

    const shouldDivide = mutedTracks.length > 0 && solodTracks.length > 0;

    return (
        <div
            style={{
                position: "absolute",
                maxWidth: "15%",
                padding: "15px",
                borderRadius: "5px",
                backgroundColor: "#323232dd",
                bottom: "2%",
                left: "1%"
            }}
        >
            { mutedTracks.length > 0 && <TrackList tracks={mutedTracks} icon={<h2 style={{color: "#cc3b3b"}}>M</h2>}/>}
            { (shouldDivide) && <hr style={{color: "#c2c2c2"}}/>}
            { solodTracks.length > 0 && <TrackList tracks={solodTracks} icon={<h2 style={{paddingLeft: "2%", color: "#928b00"}}>S</h2>}/>}
        </div>
    );
}
