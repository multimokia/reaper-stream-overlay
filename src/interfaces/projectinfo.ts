export interface ProjectInfo {
    project_name: string,
    selected_media_items: MediaItemInfo[]
}

export type MediaItemInfo = {
    track_name: string,
    track_color: number[],
    start_time: number,
    end_time: number
}
