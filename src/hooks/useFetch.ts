import { useEffect, useState } from "react";
import axios from "axios";

export function useFetch<T>(url: string) {
    const [data, setData] = useState<T>({project_name: "", selected_media_items: []} as T);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        setLoading(true);
        axios
            .get(url, {headers: {"Access-Control-Allow-Origin": "*"}})
            .then((response) => {
                setData(response.data);
            })
            .catch((err) => {
                setError(err);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [url]);

    const refetch = () => {
        setLoading(true);
        axios
            .get(url, {headers: {"Access-Control-Allow-Origin": "*"}})
            .then((response) => {
                setData(response.data);
            })
            .catch((err) => {
                setError(err);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return { data, loading, error, refetch };
}
