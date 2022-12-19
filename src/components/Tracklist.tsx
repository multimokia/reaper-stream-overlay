import { ReactNode } from "react";
import { ShortTrackInfo } from "../interfaces/projectinfo";

export const TrackList: React.FC<{ tracks: ShortTrackInfo[], icon: ReactNode }> = ({tracks, icon}) => {
    return (
        <>
            {tracks.map((value) => (
                <div
                    style={{
                        display: "flex",
                        flex: 1,
                        textAlign: "center",
                        verticalAlign: "middle",
                        color: "#c2c2c2",
                        animation: "fade 0.5s linear"
                    }}
                >
                    {icon}
                    <h4 style={{alignSelf: "center", paddingLeft: "2em"}}>{value.track_name}</h4>
                </div>
            ))}
        </>
    )
}
