import { Carousel } from 'react-bootstrap';
import { MediaItemInfo } from '../interfaces/projectinfo';
import * as Icon from 'react-bootstrap-icons';

export const TopBanner: React.FC<{selectedItemInfo: MediaItemInfo | undefined, projectTitle: string}> = ({selectedItemInfo, projectTitle}) => {
    const [r, g, b] = selectedItemInfo === undefined ? [33, 33, 33] : selectedItemInfo.track_color;

    return (
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
                <h1>{projectTitle}</h1>
            </Carousel.Item>
            <Carousel.Item
                style={{
                    background: `rgb(${r}, ${g}, ${b})`
                }}
            >
                <h1>{selectedItemInfo === undefined ? "No item selected" : `Editing ${selectedItemInfo.track_name} | ${new Date(selectedItemInfo.start_time * 1000).toISOString().substring(14, 19)} - ${new Date(selectedItemInfo.end_time * 1000).toISOString().substring(14, 19)}`}</h1>
            </Carousel.Item>
            <Carousel.Item
            >
                <h1><table width={"100%"}><td><Icon.Twitter/> @multimokia</td><td><Icon.Youtube/> Subscribe!</td></table></h1>
            </Carousel.Item>
        </Carousel>
    )
}
