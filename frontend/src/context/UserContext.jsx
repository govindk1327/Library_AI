import { createContext, useContext, useEffect, useState } from "react";
import client from "../api/client";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [preferences, setPreferences] = useState(null);
    const [user, setUser] = useState(null); // optional: can expand later

    useEffect(() => {
        async function fetchPrefs() {
            try {
                const res = await client.get("/preferences/");
                setPreferences(res.data);
            } catch {
                setPreferences({ preferred_language: "ko" }); // default
            }
        }

        async function fetchUser() {
            try {
                const res = await client.get("/me/");
                setUser(res.data);
            } catch {
                setUser(null);
            }
        }

        fetchPrefs();
        fetchUser();
    }, []);

    const updatePreferences = async (newPrefs) => {
        try {
            const res = await client.patch("/preferences/", newPrefs);
            setPreferences((prev) => ({ ...prev, ...res.data }));
        } catch (err) {
            console.error("❌ Failed to update preferences:", err);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        setPreferences({ preferred_language: "ko" }); // reset default
    };

    return (
        <UserContext.Provider value={{
            preferences,
            updatePreferences,
            user,
            logout
        }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUserPrefs = () => useContext(UserContext);
