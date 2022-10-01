export interface ProjectInfo {
    project_name: string,
    selected_media_items: MediaItemInfo[]
}

export interface MediaItemInfo {
    track_name: string,
    track_color: number[],
    start_time: number,
    end_time: number
}
